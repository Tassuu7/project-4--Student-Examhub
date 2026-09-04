/**
 * ExamHub - Student Results & Scorecards List
 * Displays all completed and graded assessments with instant access to detailed scorecards.
 */

import React, { useState, useEffect } from 'react';
import {
  Award,
  BookOpen,
  Calendar,
  CheckCircle2,
  XCircle,
  TrendingUp,
  FileText,
  Search,
} from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';
import { examService } from '../../services/examService';
import { ExamResult } from '../../types/exam';
import { LoadingSpinner } from '../common/LoadingSpinner';

interface StudentResultsListProps {
  onViewScorecard: (attemptId: string) => void;
}

export const StudentResultsList: React.FC<StudentResultsListProps> = ({ onViewScorecard }) => {
  const { user } = useAuth();
  const [completedExams, setCompletedExams] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    const fetchResults = async () => {
      try {
        setLoading(true);
        const res = await examService.getStudentAssignedExams();
        const completed = (res.items || []).filter(
          (e) =>
            e.attempt_status === 'submitted' ||
            e.attempt_status === 'auto_submitted' ||
            e.attempt_status === 'evaluated'
        );
        setCompletedExams(completed);
      } catch {
        setCompletedExams([]);
      } finally {
        setLoading(false);
      }
    };

    fetchResults();
  }, [user]);

  const filtered = completedExams.filter(
    (e) =>
      e.name.toLowerCase().includes(search.toLowerCase()) ||
      (e.subject_code && e.subject_code.toLowerCase().includes(search.toLowerCase())) ||
      (e.subject_name && e.subject_name.toLowerCase().includes(search.toLowerCase()))
  );

  if (loading) {
    return (
      <div className="py-16 flex justify-center">
        <LoadingSpinner size="md" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-stone-200 dark:border-zinc-800 pb-5">
        <div>
          <h2 className="text-xl font-bold text-stone-900 dark:text-stone-100 flex items-center gap-2">
            <FileText className="w-5 h-5 text-amber-600" />
            My Examination Results & Scorecards
          </h2>
          <p className="text-xs text-stone-500 dark:text-zinc-400 mt-1">
            Official grades, question-by-question evaluations, and class rank distributions.
          </p>
        </div>

        <div className="relative w-full sm:w-64">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-stone-400" />
          <input
            type="text"
            placeholder="Search completed exams..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 text-xs rounded-lg border border-stone-200 dark:border-zinc-700 bg-stone-50 dark:bg-zinc-800 text-stone-900 dark:text-stone-100 placeholder-stone-400 focus:outline-none focus:ring-2 focus:ring-amber-500"
          />
        </div>
      </div>

      {filtered.length === 0 ? (
        <div className="text-center py-16 px-4 rounded-2xl border border-dashed border-stone-300 dark:border-zinc-700 bg-white dark:bg-zinc-900">
          <FileText className="w-10 h-10 mx-auto text-stone-400 mb-2" />
          <h3 className="text-sm font-semibold text-stone-900 dark:text-stone-100">
            No completed assessments yet
          </h3>
          <p className="text-xs text-stone-500 max-w-sm mx-auto mt-1">
            Complete your scheduled examinations to have your evaluations and scorecards posted here.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filtered.map((exam) => (
            <div
              key={exam.id}
              className="p-5 rounded-2xl border border-stone-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 shadow-xs flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between gap-2 mb-2">
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 dark:bg-emerald-950/50 dark:text-emerald-300">
                    {exam.subject_code}
                  </span>
                  <span
                    className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded ${
                      exam.pass_fail === 'PASS'
                        ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                        : 'bg-rose-50 text-rose-700 border border-rose-200'
                    }`}
                  >
                    {exam.pass_fail || 'EVALUATED'}
                  </span>
                </div>

                <h3 className="text-base font-bold text-stone-900 dark:text-stone-100">
                  {exam.name}
                </h3>
                <p className="text-xs text-stone-500 mt-0.5">
                  {exam.subject_name}
                </p>

                <div className="grid grid-cols-3 gap-2 mt-4 p-3 rounded-xl bg-stone-50 dark:bg-zinc-800/60 border border-stone-100 dark:border-zinc-800/80 text-center">
                  <div>
                    <span className="text-[10px] text-stone-400 block">Score</span>
                    <strong className="text-xs font-bold text-stone-900 dark:text-stone-100">
                      {exam.obtained_marks !== undefined ? `${exam.obtained_marks}/${exam.total_marks}` : 'N/A'}
                    </strong>
                  </div>
                  <div>
                    <span className="text-[10px] text-stone-400 block">Percentage</span>
                    <strong className="text-xs font-bold text-emerald-600">
                      {exam.percentage !== undefined ? `${exam.percentage.toFixed(1)}%` : 'N/A'}
                    </strong>
                  </div>
                  <div>
                    <span className="text-[10px] text-stone-400 block">Grade</span>
                    <strong className="text-xs font-bold text-amber-600">
                      {exam.grade || 'A'}
                    </strong>
                  </div>
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-stone-100 dark:border-zinc-800 flex items-center justify-between">
                <span className="text-[11px] text-stone-400">
                  Class Rank: <strong className="text-stone-700 dark:text-zinc-200">#{exam.rank || 1}</strong>
                </span>
                <button
                  onClick={() => exam.attempt_id && onViewScorecard(exam.attempt_id)}
                  className="px-3 py-1.5 text-xs font-semibold rounded-lg bg-stone-900 hover:bg-stone-800 dark:bg-stone-100 dark:hover:bg-white text-white dark:text-stone-900 transition-colors"
                >
                  View Full Scorecard
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
