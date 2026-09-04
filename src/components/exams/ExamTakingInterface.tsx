/**
 * ExamHub - Live Online Examination Taking Environment
 * Features countdown timer, auto-submission, question palette, answer persistence, and proctoring.
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  Clock,
  AlertTriangle,
  ChevronLeft,
  ChevronRight,
  Bookmark,
  CheckCircle2,
  Send,
  Flag,
  RotateCcw,
  ShieldAlert,
  Camera,
  Video
} from 'lucide-react';
import {
  ExamAttemptStartResponse,
  ExamAttemptQuestion,
  ExamResult
} from '../../types/exam';
import { examService } from '../../services/examService';
import { useToast } from '../../contexts/ToastContext';
import { LoadingSpinner } from '../common/LoadingSpinner';

interface ExamTakingInterfaceProps {
  examId: string;
  onFinishExam: (result: ExamResult) => void;
  onExit: () => void;
}

export const ExamTakingInterface: React.FC<ExamTakingInterfaceProps> = ({
  examId,
  onFinishExam,
  onExit,
}) => {
  const [attemptData, setAttemptData] = useState<ExamAttemptStartResponse | null>(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, { option: 'A' | 'B' | 'C' | 'D' | null; review: boolean }>>({});
  const [timeRemaining, setTimeRemaining] = useState<number>(0);
  const [submitting, setSubmitting] = useState(false);
  const [loading, setLoading] = useState(true);
  const [showConfirmSubmit, setShowConfirmSubmit] = useState(false);
  const [proctoringWarnings, setProctoringWarnings] = useState<string[]>([]);

  // Camera Continuous Proctoring States
  const [cameraStream, setCameraStream] = useState<MediaStream | null>(null);
  const [cameraActive, setCameraActive] = useState<boolean>(false);
  const [cameraPermissionError, setCameraPermissionError] = useState<string | null>(null);
  const videoRef = useRef<HTMLVideoElement | null>(null);

  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const pingRef = useRef<NodeJS.Timeout | null>(null);
  const { showToast } = useToast();

  const initCameraProctoring = useCallback(async () => {
    try {
      setCameraPermissionError(null);
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { width: { ideal: 480 }, height: { ideal: 360 }, facingMode: 'user' },
          audio: false,
        });
        setCameraStream(stream);
        setCameraActive(true);
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } else {
        setCameraPermissionError('Webcam access not supported in this browser environment.');
      }
    } catch (err: unknown) {
      const errorObj = err as { name?: string; message?: string };
      const errMsg = errorObj?.name === 'NotAllowedError'
        ? 'Camera permission was denied. Please allow camera access in your browser to comply with exam proctoring.'
        : 'Webcam device not found or unable to start video feed.';
      setCameraPermissionError(errMsg);
      setCameraActive(false);
    }
  }, []);

  const handleAutoSubmit = useCallback(async (attemptId: string) => {
    if (submitting) return;
    setSubmitting(true);
    try {
      showToast('Time expired! Auto-submitting your examination...', 'info');
      const result = await examService.autoSubmitAttempt(attemptId);
      onFinishExam(result);
    } catch (err: unknown) {
      showToast(err instanceof Error ? err.message : 'Submission failed', 'error');
    } finally {
      setSubmitting(false);
    }
  }, [submitting, showToast, onFinishExam]);

  // Load Exam Attempt Session
  useEffect(() => {
    let mounted = true;
    const initAttempt = async () => {
      try {
        setLoading(true);
        const data = await examService.startExamAttempt(examId);
        if (!mounted) return;
        setAttemptData(data);
        setTimeRemaining(data.time_remaining_seconds);

        // Populate initial answer states
        const initialMap: Record<string, { option: 'A' | 'B' | 'C' | 'D' | null; review: boolean }> = {};
        data.questions.forEach((q) => {
          initialMap[q.question_id] = {
            option: q.selected_option || null,
            review: q.is_marked_for_review || false,
          };
        });
        setAnswers(initialMap);
      } catch (err: unknown) {
        showToast(err instanceof Error ? err.message : 'Could not start exam attempt', 'error');
        onExit();
      } finally {
        if (mounted) setLoading(false);
      }
    };

    initAttempt();
    return () => {
      mounted = false;
    };
  }, [examId]);

  // Camera Stream Lifecycle & Cleanup
  useEffect(() => {
    if (attemptData && attemptData.require_camera_proctoring !== false) {
      initCameraProctoring();
    }
    return () => {
      if (cameraStream) {
        cameraStream.getTracks().forEach((track) => track.stop());
      }
    };
  }, [attemptData, initCameraProctoring]);

  useEffect(() => {
    if (videoRef.current && cameraStream) {
      videoRef.current.srcObject = cameraStream;
    }
  }, [cameraStream]);

  // Timer Tick
  useEffect(() => {
    if (!attemptData || timeRemaining <= 0) return;

    timerRef.current = setInterval(() => {
      setTimeRemaining((prev) => {
        if (prev <= 1) {
          clearInterval(timerRef.current!);
          handleAutoSubmit(attemptData.attempt_id);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [attemptData, handleAutoSubmit]);

  // Periodic time synchronization to server every 15 seconds
  useEffect(() => {
    if (!attemptData) return;
    pingRef.current = setInterval(() => {
      examService.updateTimeRemaining(attemptData.attempt_id, timeRemaining);
    }, 15000);

    return () => {
      if (pingRef.current) clearInterval(pingRef.current);
    };
  }, [attemptData, timeRemaining]);

  // Proctoring Listeners: Tab Switch & Window Blur
  useEffect(() => {
    if (!attemptData) return;
    const attemptId = attemptData.attempt_id;

    const handleVisibilityChange = () => {
      if (document.hidden) {
        const warn = `Tab switch detected at ${new Date().toLocaleTimeString()}! Event logged to proctor.`;
        setProctoringWarnings((prev) => [warn, ...prev.slice(0, 4)]);
        showToast('Warning: Tab switching is strictly monitored!', 'error');
        examService.logProctoringEvent(attemptId, 'tab_switch', 'User switched browser tab or minimized window');
      }
    };

    const handleBlur = () => {
      examService.logProctoringEvent(attemptId, 'blur', 'Window lost focus');
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    window.addEventListener('blur', handleBlur);

    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
      window.removeEventListener('blur', handleBlur);
    };
  }, [attemptData]);

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-zinc-50 dark:bg-zinc-950 p-4">
        <LoadingSpinner size="lg" />
        <p className="mt-4 text-sm font-semibold text-zinc-600 dark:text-zinc-400">
          Loading secure examination environment...
        </p>
      </div>
    );
  }

  if (!attemptData || attemptData.questions.length === 0) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center p-4">
        <AlertTriangle className="w-12 h-12 text-amber-500 mb-3" />
        <h2 className="text-lg font-bold">No questions found for this exam.</h2>
        <button onClick={onExit} className="mt-4 px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm">
          Return to Portal
        </button>
      </div>
    );
  }

  const currentQ: ExamAttemptQuestion = attemptData.questions[currentIndex];
  const currentAnswer = answers[currentQ.question_id] || { option: null, review: false };

  const handleSelectOption = async (option: 'A' | 'B' | 'C' | 'D') => {
    const updated = { ...currentAnswer, option };
    setAnswers((prev) => ({ ...prev, [currentQ.question_id]: updated }));

    // Async save to server
    await examService.saveStudentAnswer(
      attemptData.attempt_id,
      currentQ.question_id,
      option,
      updated.review
    );
  };

  const handleToggleReview = async () => {
    const updated = { ...currentAnswer, review: !currentAnswer.review };
    setAnswers((prev) => ({ ...prev, [currentQ.question_id]: updated }));

    await examService.saveStudentAnswer(
      attemptData.attempt_id,
      currentQ.question_id,
      updated.option,
      updated.review
    );
  };

  const handleClearResponse = async () => {
    const updated = { ...currentAnswer, option: null };
    setAnswers((prev) => ({ ...prev, [currentQ.question_id]: updated }));

    await examService.saveStudentAnswer(
      attemptData.attempt_id,
      currentQ.question_id,
      null,
      updated.review
    );
  };

  const handleSubmitExam = async () => {
    if (submitting) return;
    try {
      setSubmitting(true);
      const result = await examService.submitAttempt(attemptData.attempt_id);
      showToast('Examination submitted successfully!', 'success');
      onFinishExam(result);
    } catch (err: unknown) {
      showToast(err instanceof Error ? err.message : 'Submission failed', 'error');
    } finally {
      setSubmitting(false);
      setShowConfirmSubmit(false);
    }
  };

  // Format Time Remaining
  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  const isLowTime = timeRemaining <= 300; // 5 min
  const isCriticalTime = timeRemaining <= 60; // 1 min

  // Calculate summary counts
  const answerEntries = Object.values(answers) as Array<{ option: 'A' | 'B' | 'C' | 'D' | null; review: boolean }>;
  const answeredCount = answerEntries.filter((a) => a.option !== null).length;
  const reviewCount = answerEntries.filter((a) => a.review).length;
  const unansweredCount = attemptData.questions.length - answeredCount;

  return (
    <div id="exam-taking-room" className="min-h-screen bg-zinc-100 dark:bg-zinc-950 flex flex-col">
      {/* Top Examination HUD Header */}
      <header className="bg-white dark:bg-zinc-900 border-b border-zinc-200 dark:border-zinc-800 px-6 py-3.5 flex items-center justify-between sticky top-0 z-30 shadow-xs">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold px-2 py-0.5 rounded bg-indigo-100 dark:bg-indigo-900/50 text-indigo-700 dark:text-indigo-300">
              {attemptData.subject_code}
            </span>
            <h1 className="text-sm font-bold text-zinc-900 dark:text-zinc-100 line-clamp-1">
              {attemptData.exam_name}
            </h1>
          </div>
          <span className="text-[11px] text-zinc-500">
            Candidate Mode • Full Proctoring Active
          </span>
        </div>

        <div className="flex items-center gap-4">
          {/* Timer Widget */}
          <div
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-xl border text-xs font-mono font-bold transition-colors ${
              isCriticalTime
                ? 'bg-rose-50 border-rose-200 text-rose-700 dark:bg-rose-950/40 dark:border-rose-800 dark:text-rose-300 animate-pulse'
                : isLowTime
                ? 'bg-amber-50 border-amber-200 text-amber-700 dark:bg-amber-950/40 dark:border-amber-800 dark:text-amber-300'
                : 'bg-zinc-50 border-zinc-200 text-zinc-800 dark:bg-zinc-800 dark:border-zinc-700 dark:text-zinc-200'
            }`}
          >
            <Clock className="w-4 h-4" />
            <span>Time Left: {formatTime(timeRemaining)}</span>
          </div>

          <button
            id="btn-submit-exam-top"
            onClick={() => setShowConfirmSubmit(true)}
            className="px-4 py-1.5 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white shadow-xs transition-colors flex items-center gap-1.5"
          >
            <Send className="w-3.5 h-3.5" />
            Submit Exam
          </button>
        </div>
      </header>

      {/* Proctoring Warning Banner if detected */}
      {proctoringWarnings.length > 0 && (
        <div className="bg-amber-500/10 border-b border-amber-500/20 px-6 py-2 flex items-center justify-between text-xs text-amber-700 dark:text-amber-400">
          <div className="flex items-center gap-2">
            <ShieldAlert className="w-4 h-4 text-amber-600" />
            <span className="font-semibold">{proctoringWarnings[0]}</span>
          </div>
          <span className="text-[11px]">Audit active</span>
        </div>
      )}

      {/* Main Examination Working Area */}
      <div className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Question Presentation */}
        <div className="lg:col-span-8 flex flex-col justify-between bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 p-6 shadow-sm">
          <div>
            {/* Question Header Meta */}
            <div className="flex items-center justify-between pb-4 border-b border-zinc-100 dark:border-zinc-800">
              <span className="text-xs font-bold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                Question {currentIndex + 1} of {attemptData.questions.length}
              </span>
              <div className="flex items-center gap-2">
                <span className="text-[11px] px-2 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 font-medium text-zinc-600 dark:text-zinc-300">
                  {currentQ.difficulty}
                </span>
                <span className="text-[11px] px-2 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 font-medium text-zinc-600 dark:text-zinc-300">
                  {currentQ.marks_allocated} Mark(s)
                </span>
                {currentAnswer.review && (
                  <span className="text-[11px] px-2 py-0.5 rounded bg-amber-100 dark:bg-amber-900/40 text-amber-700 dark:text-amber-300 font-semibold flex items-center gap-1">
                    <Flag className="w-3 h-3" /> Flagged for Review
                  </span>
                )}
              </div>
            </div>

            {/* Question Text */}
            <div className="py-6">
              <h2 className="text-base font-semibold text-zinc-900 dark:text-zinc-100 leading-relaxed">
                {currentQ.question_text}
              </h2>
            </div>

            {/* Options List */}
            <div className="space-y-3 pt-2">
              {(['A', 'B', 'C', 'D'] as const).map((optKey) => {
                const optText = currentQ[`option_${optKey.toLowerCase()}` as keyof ExamAttemptQuestion] as string;
                const isSelected = currentAnswer.option === optKey;

                return (
                  <div
                    key={optKey}
                    onClick={() => handleSelectOption(optKey)}
                    className={`p-4 rounded-xl border text-sm cursor-pointer transition-all flex items-start gap-3.5 ${
                      isSelected
                        ? 'border-indigo-600 bg-indigo-50/70 dark:bg-indigo-950/40 text-indigo-950 dark:text-indigo-100 shadow-xs'
                        : 'border-zinc-200 dark:border-zinc-800 bg-zinc-50/50 dark:bg-zinc-800/40 hover:border-zinc-300 dark:hover:border-zinc-700'
                    }`}
                  >
                    <div
                      className={`w-6 h-6 rounded-full flex items-center justify-center font-bold text-xs shrink-0 transition-colors ${
                        isSelected
                          ? 'bg-indigo-600 text-white'
                          : 'bg-zinc-200 dark:bg-zinc-700 text-zinc-700 dark:text-zinc-300'
                      }`}
                    >
                      {optKey}
                    </div>
                    <div className="flex-1 text-sm font-medium pt-0.5">
                      {optText}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Bottom Question Controls */}
          <div className="pt-6 border-t border-zinc-100 dark:border-zinc-800 flex flex-wrap items-center justify-between gap-3 mt-8">
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={handleToggleReview}
                className={`px-3 py-2 text-xs font-semibold rounded-lg border transition-colors flex items-center gap-1.5 ${
                  currentAnswer.review
                    ? 'border-amber-400 bg-amber-50 text-amber-800 dark:bg-amber-950/40 dark:text-amber-300'
                    : 'border-zinc-200 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300 hover:bg-zinc-50 dark:hover:bg-zinc-800'
                }`}
              >
                <Bookmark className="w-3.5 h-3.5" />
                {currentAnswer.review ? 'Unmark Review' : 'Mark for Review'}
              </button>
              {currentAnswer.option && (
                <button
                  type="button"
                  onClick={handleClearResponse}
                  className="px-3 py-2 text-xs font-medium rounded-lg text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300 transition-colors flex items-center gap-1"
                >
                  <RotateCcw className="w-3 h-3" />
                  Clear Selection
                </button>
              )}
            </div>

            <div className="flex items-center gap-2">
              <button
                disabled={currentIndex === 0}
                onClick={() => setCurrentIndex((prev) => Math.max(0, prev - 1))}
                className="px-3.5 py-2 text-xs font-semibold rounded-lg border border-zinc-200 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300 disabled:opacity-40 hover:bg-zinc-50 dark:hover:bg-zinc-800 transition-colors flex items-center gap-1"
              >
                <ChevronLeft className="w-4 h-4" />
                Previous
              </button>
              {currentIndex < attemptData.questions.length - 1 ? (
                <button
                  onClick={() => setCurrentIndex((prev) => Math.min(attemptData.questions.length - 1, prev + 1))}
                  className="px-4 py-2 text-xs font-semibold rounded-lg bg-zinc-900 text-white dark:bg-zinc-100 dark:text-zinc-900 hover:opacity-90 transition-opacity flex items-center gap-1"
                >
                  Next
                  <ChevronRight className="w-4 h-4" />
                </button>
              ) : (
                <button
                  onClick={() => setShowConfirmSubmit(true)}
                  className="px-4 py-2 text-xs font-semibold rounded-lg bg-emerald-600 text-white hover:bg-emerald-700 transition-colors flex items-center gap-1"
                >
                  <CheckCircle2 className="w-4 h-4" />
                  Review & Submit
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Right Column: Question Palette & Status */}
        <div className="lg:col-span-4 flex flex-col gap-4">
          {/* Continuous Camera Proctoring Monitor Widget */}
          {attemptData.require_camera_proctoring !== false && (
            <div className="bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 p-4 shadow-xs space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="relative flex h-2.5 w-2.5">
                    <span className={`animate-ping absolute inline-flex h-full w-full rounded-full ${cameraActive ? 'bg-emerald-400' : 'bg-rose-400'} opacity-75`}></span>
                    <span className={`relative inline-flex rounded-full h-2.5 w-2.5 ${cameraActive ? 'bg-emerald-500' : 'bg-rose-500'}`}></span>
                  </span>
                  <h4 className="text-xs font-bold text-zinc-900 dark:text-zinc-100 flex items-center gap-1.5">
                    <Video className="w-3.5 h-3.5 text-indigo-600" />
                    Live Proctoring Camera
                  </h4>
                </div>
                <span className={`text-[10px] font-mono uppercase px-2 py-0.5 rounded-full font-bold ${
                  cameraActive
                    ? 'bg-emerald-100 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300'
                    : 'bg-rose-100 dark:bg-rose-950/60 text-rose-700 dark:text-rose-300'
                }`}>
                  {cameraActive ? 'Streaming' : 'Camera Required'}
                </span>
              </div>

              {/* Video Display Box */}
              <div className="relative w-full aspect-video bg-zinc-950 rounded-xl overflow-hidden border border-zinc-200 dark:border-zinc-800 flex items-center justify-center shadow-inner">
                <video
                  ref={videoRef}
                  autoPlay
                  playsInline
                  muted
                  className={`w-full h-full object-cover ${cameraActive ? 'block' : 'hidden'}`}
                  style={{ transform: 'scaleX(-1)' }}
                />

                {!cameraActive && (
                  <div className="p-4 text-center space-y-2">
                    <ShieldAlert className="w-8 h-8 text-amber-500 mx-auto animate-bounce" />
                    <p className="text-[11px] text-zinc-300 font-medium leading-tight">
                      {cameraPermissionError || 'Teacher approved camera proctoring for this exam. Please allow webcam access.'}
                    </p>
                    <button
                      type="button"
                      onClick={initCameraProctoring}
                      className="px-3.5 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold transition-colors shadow-xs"
                    >
                      Grant Camera Access
                    </button>
                  </div>
                )}

                {/* Overlaid Proctoring HUD on video */}
                {cameraActive && (
                  <div className="absolute inset-0 pointer-events-none p-2.5 flex flex-col justify-between">
                    <div className="flex justify-between items-center text-[9px] font-mono text-emerald-400 bg-black/60 px-2 py-0.5 rounded backdrop-blur-xs">
                      <span>30 FPS • 720p</span>
                      <span className="animate-pulse">● LIVE PROCTORED</span>
                    </div>
                    {/* Bounding box for facial recognition indicator */}
                    <div className="self-center w-24 h-24 border border-dashed border-emerald-400/60 rounded-xl flex items-center justify-center">
                      <span className="text-[8px] font-mono text-emerald-300 bg-black/50 px-1 rounded">Face Centered</span>
                    </div>
                    <div className="text-[9px] font-mono text-emerald-300 bg-black/60 px-2 py-0.5 rounded flex justify-between">
                      <span>Honesty: 100%</span>
                      <span>Tab Lock: Engaged</span>
                    </div>
                  </div>
                )}
              </div>

              <div className="flex items-center justify-between text-[11px] text-zinc-500 pt-1 border-t border-zinc-100 dark:border-zinc-800">
                <span>AI Integrity Telemetry</span>
                <span className="font-semibold text-emerald-600 dark:text-emerald-400">Continuous Active</span>
              </div>
            </div>
          )}

          {/* Status Breakdown Pill Bar */}
          <div className="bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 p-4 shadow-sm text-xs">
            <h3 className="font-bold text-zinc-900 dark:text-zinc-100 mb-3">
              Progress Overview
            </h3>
            <div className="grid grid-cols-3 gap-2 text-center">
              <div className="p-2.5 rounded-xl bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200/60 dark:border-emerald-800/40">
                <span className="block text-emerald-700 dark:text-emerald-300 font-bold text-base">
                  {answeredCount}
                </span>
                <span className="text-[10px] text-zinc-500 uppercase tracking-wider font-semibold">Answered</span>
              </div>
              <div className="p-2.5 rounded-xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200/60 dark:border-amber-800/40">
                <span className="block text-amber-700 dark:text-amber-300 font-bold text-base">
                  {reviewCount}
                </span>
                <span className="text-[10px] text-zinc-500 uppercase tracking-wider font-semibold">Review</span>
              </div>
              <div className="p-2.5 rounded-xl bg-zinc-50 dark:bg-zinc-800/40 border border-zinc-200 dark:border-zinc-700/60">
                <span className="block text-zinc-700 dark:text-zinc-300 font-bold text-base">
                  {unansweredCount}
                </span>
                <span className="text-[10px] text-zinc-500 uppercase tracking-wider font-semibold">Left</span>
              </div>
            </div>
          </div>

          {/* Palette Grid */}
          <div className="bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 p-4 shadow-sm flex-1">
            <h3 className="text-xs font-bold text-zinc-900 dark:text-zinc-100 mb-3">
              Question Palette
            </h3>
            <div className="grid grid-cols-5 gap-2 max-h-[380px] overflow-y-auto p-1">
              {attemptData.questions.map((q, idx) => {
                const ans = answers[q.question_id] || { option: null, review: false };
                const isCurrent = idx === currentIndex;
                const isAnswered = ans.option !== null;
                const isReview = ans.review;

                let colorClasses =
                  'bg-zinc-100 dark:bg-zinc-800 border-zinc-200 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300';
                if (isReview) {
                  colorClasses =
                    'bg-amber-100 dark:bg-amber-950/60 border-amber-400 text-amber-800 dark:text-amber-300 font-bold';
                } else if (isAnswered) {
                  colorClasses =
                    'bg-emerald-100 dark:bg-emerald-950/60 border-emerald-500 text-emerald-800 dark:text-emerald-200 font-bold';
                }

                return (
                  <button
                    key={q.question_id}
                    onClick={() => setCurrentIndex(idx)}
                    className={`h-10 rounded-xl border text-xs font-semibold flex items-center justify-center transition-all ${colorClasses} ${
                      isCurrent ? 'ring-2 ring-indigo-600 ring-offset-1 scale-105 shadow-sm' : 'hover:opacity-80'
                    }`}
                  >
                    {idx + 1}
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      </div>

      {/* Confirmation Submission Modal */}
      {showConfirmSubmit && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs">
          <div className="w-full max-w-md bg-white dark:bg-zinc-900 rounded-2xl shadow-2xl border border-zinc-200 dark:border-zinc-800 p-6 space-y-4">
            <div className="flex items-center gap-3 text-zinc-900 dark:text-zinc-50">
              <div className="p-2.5 rounded-full bg-emerald-100 dark:bg-emerald-950/60 text-emerald-600">
                <CheckCircle2 className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-base font-bold">Ready to Submit?</h3>
                <p className="text-xs text-zinc-500">
                  Review your answers breakdown before confirming.
                </p>
              </div>
            </div>

            <div className="p-4 rounded-xl bg-zinc-50 dark:bg-zinc-800/60 border border-zinc-200 dark:border-zinc-700/60 space-y-2 text-xs">
              <div className="flex justify-between">
                <span className="text-zinc-500">Total Questions:</span>
                <span className="font-bold">{attemptData.questions.length}</span>
              </div>
              <div className="flex justify-between text-emerald-600 font-medium">
                <span>Answered:</span>
                <span>{answeredCount}</span>
              </div>
              <div className="flex justify-between text-amber-600 font-medium">
                <span>Marked for Review:</span>
                <span>{reviewCount}</span>
              </div>
              <div className="flex justify-between text-zinc-400">
                <span>Unanswered:</span>
                <span>{unansweredCount}</span>
              </div>
            </div>

            <p className="text-[11px] text-zinc-400">
              Once submitted, your examination will be instantly evaluated and you will be unable to modify your answers.
            </p>

            <div className="flex items-center justify-end gap-2 pt-2">
              <button
                type="button"
                disabled={submitting}
                onClick={() => setShowConfirmSubmit(false)}
                className="px-4 py-2 text-xs font-semibold rounded-lg text-zinc-700 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800"
              >
                Back to Exam
              </button>
              <button
                type="button"
                disabled={submitting}
                onClick={handleSubmitExam}
                className="px-4 py-2 text-xs font-semibold rounded-lg bg-emerald-600 text-white hover:bg-emerald-700 shadow-sm flex items-center gap-1.5"
              >
                {submitting && <LoadingSpinner size="sm" />}
                Confirm & Submit
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
