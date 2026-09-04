/**
 * ExamHub - Student Examination Portal
 * Shows assigned exams, schedules, active examinations, and scorecards.
 */

import React, { useState, useEffect } from 'react';
import {
  Clock,
  Award,
  Calendar,
  PlayCircle,
  FileCheck,
  CheckCircle2,
  AlertCircle,
  TrendingUp
} from 'lucide-react';
import { StudentPortalExam } from '../../types/exam';
import { examService } from '../../services/examService';
import { useToast } from '../../contexts/ToastContext';
import { LoadingSpinner } from '../common/LoadingSpinner';

interface StudentExamPortalProps {
  onStartExam: (examId: string) => void;
  onViewResult: (attemptId: string) => void;
}

export const StudentExamPortal: React.FC<StudentExamPortalProps> = ({
  onStartExam,
  onViewResult,
}) => {
  const [exams, setExams] = useState<StudentPortalExam[]>([]);
  const [loading, setLoading] = useState(true);

  const { showToast } = useToast();

  const loadStudentExams = async () => {
    try {
      setLoading(true);
      const res = await examService.getStudentAssignedExams();
      setExams(res.items || []);
    } catch (err: unknown) {
      showToast(err instanceof Error ? err.message : 'Failed to load examinations', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStudentExams();
  }, []);

  const getStatusBadge = (exam: StudentPortalExam) => {
    if (exam.attempt_status === 'submitted' || exam.attempt_status === 'auto_submitted' || exam.attempt_status === 'evaluated') {
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300">
          <CheckCircle2 className="w-3.5 h-3.5" />
          Completed
        </span>
      );
    }
    if (exam.attempt_status === 'in_progress') {
      return (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-300">
          <span className="w-1.5 h-1.5 rounded-full bg-amber-500 animate-ping"></span>
          In Progress
        </span>
      );
    }
    if (exam.status === 'active') {
      return (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-300">
          <span className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse"></span>
          Available Now
        </span>
      );
    }
    return (
      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-zinc-100 text-zinc-700 dark:bg-zinc-800 dark:text-zinc-300">
        Upcoming
      </span>
    );
  };

  return (
    <div id="student-portal-container" className="space-y-6">
      <div className="border-b border-zinc-200 dark:border-zinc-800 pb-5">
        <h1 className="text-2xl font-bold tracking-tight text-zinc-900 dark:text-zinc-50">
          My Examinations
        </h1>
        <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-1">
          Attend scheduled timed examinations, resume active sessions, and inspect your performance scorecards.
        </p>
      </div>

      {loading ? (
        <div className="py-20 flex justify-center">
          <LoadingSpinner size="lg" />
        </div>
      ) : exams.length === 0 ? (
        <div className="text-center py-16 px-4 rounded-xl border border-dashed border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-900/30">
          <FileCheck className="w-12 h-12 mx-auto text-zinc-400 mb-3" />
          <h3 className="text-base font-semibold text-zinc-900 dark:text-zinc-100">
            No examinations assigned
          </h3>
          <p className="text-sm text-zinc-500 dark:text-zinc-400 max-w-sm mx-auto mt-1">
            You do not currently have any scheduled or active examinations assigned to your student roll.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {exams.map((exam) => {
            const isCompleted =
              exam.attempt_status === 'submitted' ||
              exam.attempt_status === 'auto_submitted' ||
              exam.attempt_status === 'evaluated';
            const isInProgress = exam.attempt_status === 'in_progress';
            const isOpen = exam.status === 'active' && !isCompleted;

            return (
              <div
                key={exam.id}
                id={`student-exam-card-${exam.id}`}
                className="flex flex-col justify-between p-5 rounded-2xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 shadow-sm hover:shadow-md transition-shadow"
              >
                <div>
                  <div className="flex items-start justify-between gap-2 mb-3">
                    <span className="text-xs font-semibold px-2 py-0.5 rounded bg-indigo-50 text-indigo-700 dark:bg-indigo-950/40 dark:text-indigo-300">
                      {exam.subject_code}
                    </span>
                    {getStatusBadge(exam)}
                  </div>

                  <h3 className="text-base font-bold text-zinc-900 dark:text-zinc-50 line-clamp-1">
                    {exam.name}
                  </h3>
                  <p className="text-xs text-zinc-500 dark:text-zinc-400 line-clamp-2 mt-1 min-h-[32px]">
                    {exam.description || `Assessment for ${exam.subject_name}`}
                  </p>

                  <div className="grid grid-cols-2 gap-2 mt-4 pt-3 border-t border-zinc-100 dark:border-zinc-800 text-xs text-zinc-600 dark:text-zinc-300">
                    <div className="flex items-center gap-1.5">
                      <Clock className="w-3.5 h-3.5 text-zinc-400" />
                      <span>{exam.duration_minutes} Mins</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <Award className="w-3.5 h-3.5 text-zinc-400" />
                      <span>Pass: {exam.passing_percentage}%</span>
                    </div>
                  </div>

                  {/* Performance preview if completed */}
                  {isCompleted && exam.percentage !== undefined && (
                    <div className="mt-3.5 p-2.5 rounded-xl bg-zinc-50 dark:bg-zinc-800/60 border border-zinc-200 dark:border-zinc-700/60 flex items-center justify-between text-xs">
                      <div>
                        <span className="text-zinc-500">Score:</span>{' '}
                        <strong className="text-zinc-900 dark:text-zinc-100">
                          {exam.obtained_marks} / {exam.total_marks}
                        </strong>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-indigo-600 dark:text-indigo-400">
                          {exam.percentage.toFixed(1)}%
                        </span>
                        <span
                          className={`font-semibold px-1.5 py-0.5 rounded text-[10px] ${
                            exam.pass_fail === 'PASS'
                              ? 'bg-emerald-100 text-emerald-800'
                              : 'bg-rose-100 text-rose-800'
                          }`}
                        >
                          {exam.pass_fail}
                        </span>
                      </div>
                    </div>
                  )}
                </div>

                {/* Footer Actions */}
                <div className="mt-5 pt-3.5 border-t border-zinc-100 dark:border-zinc-800 flex items-center justify-end">
                  {isCompleted ? (
                    <button
                      onClick={() => exam.attempt_id && onViewResult(exam.attempt_id)}
                      className="w-full py-2 text-xs font-semibold rounded-lg bg-zinc-100 hover:bg-zinc-200 text-zinc-800 dark:bg-zinc-800 dark:text-zinc-200 dark:hover:bg-zinc-700 transition-colors flex items-center justify-center gap-1.5"
                    >
                      <TrendingUp className="w-3.5 h-3.5 text-indigo-600" />
                      View Scorecard & Review
                    </button>
                  ) : isInProgress ? (
                    <button
                      onClick={() => onStartExam(exam.id)}
                      className="w-full py-2 text-xs font-semibold rounded-lg bg-amber-500 text-white hover:bg-amber-600 shadow-sm transition-colors flex items-center justify-center gap-1.5"
                    >
                      <PlayCircle className="w-4 h-4" />
                      Resume Examination
                    </button>
                  ) : isOpen ? (
                    <button
                      onClick={() => onStartExam(exam.id)}
                      className="w-full py-2 text-xs font-semibold rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 shadow-sm transition-colors flex items-center justify-center gap-1.5"
                    >
                      <PlayCircle className="w-4 h-4" />
                      Start Examination
                    </button>
                  ) : (
                    <span className="text-xs text-zinc-400 font-medium py-1.5">
                      Opens Soon
                    </span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
