/**
 * ExamHub - Live Proctoring & Examination Security Dashboard
 * Monitors ongoing candidate sessions, tab switching telemetry, and integrity scores.
 */

import React, { useState, useEffect } from 'react';
import {
  ShieldAlert,
  ShieldCheck,
  Eye,
  Clock,
  User,
  AlertTriangle,
  RefreshCw,
  Search,
  Video,
  Radio,
  AlertOctagon,
  CheckCircle2,
  MessageSquare,
  Ban,
  RotateCcw,
  Volume2
} from 'lucide-react';
import { proctoringService } from '../../services/proctoringService';
import { ProctoringLiveFeedResponse, CandidateIntegrityProfile } from '../../types/proctoring';
import { LoadingSpinner } from '../common/LoadingSpinner';
import { useToast } from '../../contexts/ToastContext';

export const LiveProctoringDashboard: React.FC = () => {
  const [feed, setFeed] = useState<ProctoringLiveFeedResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedAttemptId, setSelectedAttemptId] = useState<string | null>(null);
  const [candidateProfile, setCandidateProfile] = useState<CandidateIntegrityProfile | null>(null);
  const [loadingProfile, setLoadingProfile] = useState(false);

  // Intervention modal states
  const [showWarningModal, setShowWarningModal] = useState(false);
  const [warningMessage, setWarningMessage] = useState('Please face the webcam and do not switch browser windows.');
  const [terminating, setTerminating] = useState(false);

  const { showToast } = useToast();

  const loadFeed = async () => {
    try {
      const data = await proctoringService.getLiveFeed();
      setFeed(data);
      if (!selectedAttemptId && data.active_candidates && data.active_candidates.length > 0) {
        handleInspectCandidate(data.active_candidates[0].attempt_id);
      }
    } catch (err: unknown) {
      showToast('Could not refresh proctoring feed', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadFeed();
    const interval = setInterval(loadFeed, 10000); // 10s live polling
    return () => clearInterval(interval);
  }, []);

  const handleInspectCandidate = async (attemptId: string) => {
    setSelectedAttemptId(attemptId);
    try {
      setLoadingProfile(true);
      const profile = await proctoringService.getCandidateIntegrity(attemptId);
      setCandidateProfile(profile);
    } catch {
      showToast('Failed to load candidate telemetry profile', 'error');
    } finally {
      setLoadingProfile(false);
    }
  };

  const handleSendWarning = async () => {
    if (!selectedAttemptId || !warningMessage.trim()) return;
    try {
      await proctoringService.sendWarning(selectedAttemptId, warningMessage.trim());
      showToast('Formal warning dispatched to candidate screen.', 'info');
      setShowWarningModal(false);
      handleInspectCandidate(selectedAttemptId);
    } catch {
      showToast('Failed to deliver warning to candidate.', 'error');
    }
  };

  const handleTerminateAttempt = async () => {
    if (!selectedAttemptId) return;
    if (!window.confirm('Are you sure you want to terminate this candidate session for malpractice?')) {
      return;
    }
    try {
      setTerminating(true);
      await proctoringService.terminateSession(selectedAttemptId, 'Terminated by Instructor due to proctoring violation');
      showToast('Candidate attempt terminated.', 'success');
      loadFeed();
      setSelectedAttemptId(null);
      setCandidateProfile(null);
    } catch {
      showToast('Failed to terminate candidate session.', 'error');
    } finally {
      setTerminating(false);
    }
  };

  const handleClearFlags = async () => {
    if (!selectedAttemptId) return;
    try {
      await proctoringService.clearFlags(selectedAttemptId);
      showToast('Candidate security flags cleared successfully.', 'success');
      handleInspectCandidate(selectedAttemptId);
      loadFeed();
    } catch {
      showToast('Failed to clear flags.', 'error');
    }
  };

  if (loading) {
    return (
      <div className="py-24 flex flex-col items-center justify-center">
        <LoadingSpinner size="lg" />
        <p className="mt-3 text-xs font-semibold text-zinc-500 uppercase tracking-wider">
          Connecting to Proctoring Telemetry Stream...
        </p>
      </div>
    );
  }

  return (
    <div id="live-proctoring-container" className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-zinc-200 dark:border-zinc-800 pb-5">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-zinc-900 dark:text-zinc-50 flex items-center gap-2.5">
            <ShieldAlert className="w-6 h-6 text-amber-600" />
            Continuous Proctoring & Academic Honesty Monitor
          </h1>
          <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">
            Real-time candidate telemetry, window focus loss, tab switching, and anomaly detection.
          </p>
        </div>

        <button
          onClick={loadFeed}
          className="inline-flex items-center gap-1.5 px-3 py-2 text-xs font-semibold rounded-xl border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-700 dark:text-zinc-200 hover:bg-zinc-50 dark:hover:bg-zinc-700 transition-colors"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          Refresh Live Stream
        </button>
      </div>

      {/* Monitoring Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: Active Test-Takers Roster */}
        <div className="lg:col-span-7 bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 p-5 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-zinc-900 dark:text-zinc-100">
                Active Assessment Candidates ({feed?.active_sessions_count || 0})
              </h3>
              <p className="text-xs text-zinc-500">
                Real-time sessions under continuous automated proctoring
              </p>
            </div>
            {feed && feed.flagged_sessions_count > 0 && (
              <span className="px-2 py-0.5 rounded-full bg-rose-100 text-rose-800 dark:bg-rose-950/50 dark:text-rose-300 text-xs font-bold animate-pulse">
                {feed.flagged_sessions_count} Flagged Alert(s)
              </span>
            )}
          </div>

          {!feed || feed.active_candidates.length === 0 ? (
            <div className="py-16 text-center text-zinc-400 text-xs">
              No active candidates taking examinations currently.
            </div>
          ) : (
            <div className="divide-y divide-zinc-100 dark:divide-zinc-800">
              {feed.active_candidates.map((c) => {
                const isSelected = selectedAttemptId === c.attempt_id;
                const isLowScore = c.integrity_score < 70;

                return (
                  <div
                    key={c.attempt_id}
                    onClick={() => handleInspectCandidate(c.attempt_id)}
                    className={`py-3.5 px-3 rounded-xl flex items-center justify-between cursor-pointer transition-colors ${
                      isSelected
                        ? 'bg-indigo-50/80 dark:bg-indigo-950/40 border border-indigo-200 dark:border-indigo-800'
                        : 'hover:bg-zinc-50 dark:hover:bg-zinc-800/60'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-full bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 flex items-center justify-center font-bold text-xs">
                        {c.student_name.charAt(0)}
                      </div>
                      <div>
                        <h4 className="text-xs font-bold text-zinc-900 dark:text-zinc-100">
                          {c.student_name}
                        </h4>
                        <span className="text-[10px] text-zinc-400">
                          Roll: {c.roll_number} • {c.exam_name}
                        </span>
                      </div>
                    </div>

                    <div className="flex items-center gap-4 text-xs">
                      <div className="text-right">
                        <span
                          className={`font-mono font-bold block ${
                            isLowScore ? 'text-rose-600 dark:text-rose-400' : 'text-emerald-600 dark:text-emerald-400'
                          }`}
                        >
                          {c.integrity_score}% Integrity
                        </span>
                        <span className="text-[10px] text-zinc-400">
                          {c.total_warnings} warning(s)
                        </span>
                      </div>

                      <Eye className="w-4 h-4 text-zinc-400" />
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Right: Selected Candidate Detailed Telemetry Timeline & Video Monitor */}
        <div className="lg:col-span-6 bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 p-5 shadow-xs">
          <div className="flex items-center justify-between mb-3 pb-2 border-b border-zinc-100 dark:border-zinc-800">
            <h3 className="text-sm font-bold text-zinc-900 dark:text-zinc-100 flex items-center gap-2">
              <Video className="w-4 h-4 text-indigo-600" />
              Candidate Telemetry & Live Video Monitor
            </h3>
            {candidateProfile && (
              <span className="text-xs font-bold px-2 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-300">
                {candidateProfile.roll_number}
              </span>
            )}
          </div>

          {loadingProfile ? (
            <div className="py-16 flex justify-center">
              <LoadingSpinner size="md" />
            </div>
          ) : !candidateProfile ? (
            <div className="py-16 text-center text-zinc-400 text-xs">
              <Eye className="w-8 h-8 mx-auto text-zinc-300 dark:text-zinc-700 mb-2" />
              Select an active test-taker from the roster to view their live webcam feed and integrity metrics.
            </div>
          ) : (
            <div className="space-y-4">
              {/* Simulated / Live Video Camera Card */}
              <div className="relative w-full aspect-video bg-zinc-950 rounded-xl overflow-hidden border border-zinc-200 dark:border-zinc-800 shadow-inner flex flex-col justify-between p-3 text-white">
                <div className="flex justify-between items-center text-[10px] font-mono bg-black/60 px-2 py-1 rounded backdrop-blur-xs">
                  <div className="flex items-center gap-1.5">
                    <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span>LIVE WEBCAM • 720p 30FPS</span>
                  </div>
                  <span className="text-emerald-300">{candidateProfile.student_name}</span>
                </div>

                {/* Face Tracker Simulated Reticle */}
                <div className="self-center my-auto w-28 h-32 border-2 border-dashed border-emerald-400/80 rounded-2xl flex flex-col items-center justify-center p-2 bg-emerald-950/20 backdrop-blur-2xs">
                  <User className="w-8 h-8 text-emerald-400 opacity-60" />
                  <span className="text-[8px] font-mono text-emerald-300 mt-1 bg-black/60 px-1 rounded">
                    Candidate Anchored
                  </span>
                </div>

                <div className="flex justify-between items-center text-[9px] font-mono bg-black/60 px-2 py-1 rounded">
                  <div className="flex items-center gap-2">
                    <span>Gaze: Screen Centered</span>
                    <span className="text-zinc-400">•</span>
                    <span className="flex items-center gap-0.5"><Volume2 className="w-3 h-3 text-emerald-400" /> Normal</span>
                  </div>
                  <span className="text-emerald-400">AUDIT ACTIVE</span>
                </div>
              </div>

              {/* Profile Summary Badge */}
              <div
                className={`p-3.5 rounded-xl border ${
                  candidateProfile.risk_level === 'Severe' || candidateProfile.risk_level === 'High'
                    ? 'border-rose-200 bg-rose-50/70 dark:bg-rose-950/30 text-rose-900 dark:text-rose-100'
                    : candidateProfile.risk_level === 'Moderate'
                    ? 'border-amber-200 bg-amber-50/70 dark:bg-amber-950/30 text-amber-900 dark:text-amber-100'
                    : 'border-emerald-200 bg-emerald-50/70 dark:bg-emerald-950/30 text-emerald-900 dark:text-emerald-100'
                }`}
              >
                <div className="flex justify-between items-center">
                  <div>
                    <span className="text-xs font-bold uppercase tracking-wider block">
                      Integrity Risk: {candidateProfile.risk_level}
                    </span>
                    <span className="text-[11px] opacity-80">
                      {candidateProfile.is_flagged_for_manual_review
                        ? 'Flagged for Proctor Review due to anomalous telemetry'
                        : 'Clean session. Zero policy infractions detected'}
                    </span>
                  </div>
                  <span className="font-mono font-black text-2xl">
                    {candidateProfile.integrity_score.toFixed(0)}/100
                  </span>
                </div>
                <div className="grid grid-cols-3 gap-2 mt-2 pt-2 border-t border-current/20 text-[11px]">
                  <div>Tab Switches: <strong>{candidateProfile.tab_switch_count}</strong></div>
                  <div>Focus Loss: <strong>{candidateProfile.blur_count}</strong></div>
                  <div>Face Alerts: <strong>{candidateProfile.face_anomalies_count}</strong></div>
                </div>
              </div>

              {/* Teacher Intervention Controls Toolbar */}
              <div className="p-3 rounded-xl bg-zinc-50 dark:bg-zinc-800/60 border border-zinc-200 dark:border-zinc-700/60 space-y-2">
                <h4 className="text-[11px] font-bold uppercase text-zinc-500">
                  Proctor Interventions
                </h4>
                <div className="grid grid-cols-3 gap-2">
                  <button
                    type="button"
                    onClick={() => setShowWarningModal(true)}
                    className="px-2.5 py-1.5 rounded-lg bg-amber-600 hover:bg-amber-700 text-white text-xs font-semibold flex items-center justify-center gap-1 transition-colors shadow-xs"
                  >
                    <MessageSquare className="w-3 h-3" />
                    Warn
                  </button>

                  <button
                    type="button"
                    onClick={handleClearFlags}
                    className="px-2.5 py-1.5 rounded-lg border border-zinc-300 dark:border-zinc-600 hover:bg-zinc-100 dark:hover:bg-zinc-700 text-zinc-700 dark:text-zinc-200 text-xs font-semibold flex items-center justify-center gap-1 transition-colors"
                  >
                    <RotateCcw className="w-3 h-3" />
                    Clear Flags
                  </button>

                  <button
                    type="button"
                    disabled={terminating}
                    onClick={handleTerminateAttempt}
                    className="px-2.5 py-1.5 rounded-lg bg-rose-600 hover:bg-rose-700 text-white text-xs font-semibold flex items-center justify-center gap-1 transition-colors shadow-xs disabled:opacity-50"
                  >
                    <Ban className="w-3 h-3" />
                    Terminate
                  </button>
                </div>
              </div>

              {/* Event Log Stream */}
              <div className="space-y-2 max-h-52 overflow-y-auto pr-1">
                <h4 className="text-[11px] uppercase font-bold text-zinc-400">
                  Telemetry Event Stream ({candidateProfile.events.length})
                </h4>
                {candidateProfile.events.length === 0 ? (
                  <p className="text-xs text-zinc-400 py-3 text-center">
                    Clean session. No suspicious behavior recorded.
                  </p>
                ) : (
                  candidateProfile.events.map((ev) => (
                    <div
                      key={ev.id}
                      className="p-2 rounded-lg border border-zinc-100 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-800/40 text-xs flex justify-between items-start gap-2"
                    >
                      <div>
                        <span className="font-bold text-zinc-800 dark:text-zinc-200 block text-[11px]">
                          {ev.event_type}
                        </span>
                        <p className="text-[10px] text-zinc-500 leading-tight">{ev.details}</p>
                      </div>
                      <span className="text-[10px] font-mono text-zinc-400 shrink-0">
                        {ev.timestamp.slice(11, 19)}
                      </span>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Warning Dispatch Modal */}
      {showWarningModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs">
          <div className="w-full max-w-md bg-white dark:bg-zinc-900 rounded-2xl p-5 border border-zinc-200 dark:border-zinc-800 space-y-4 shadow-xl">
            <h3 className="text-sm font-bold text-zinc-900 dark:text-zinc-50 flex items-center gap-2">
              <MessageSquare className="w-4 h-4 text-amber-500" />
              Dispatch Formal Proctor Warning
            </h3>
            <p className="text-xs text-zinc-500">
              This message will flash immediately onto the candidate examination HUD.
            </p>

            <textarea
              rows={3}
              value={warningMessage}
              onChange={(e) => setWarningMessage(e.target.value)}
              className="w-full p-2.5 text-xs rounded-xl bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-amber-500"
            />

            <div className="flex justify-end gap-2 pt-1">
              <button
                type="button"
                onClick={() => setShowWarningModal(false)}
                className="px-3 py-1.5 text-xs font-semibold rounded-lg text-zinc-600 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleSendWarning}
                className="px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-amber-600 hover:bg-amber-700 text-white shadow-xs"
              >
                Dispatch Warning
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
