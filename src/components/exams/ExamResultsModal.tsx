/**
 * ExamHub - Exam Results & Candidate Leaderboard Modal
 */

import React, { useState, useEffect } from 'react';
import {
  X,
  Award,
  Trophy,
  Users,
  CheckCircle2,
  XCircle,
  ShieldAlert,
  Search,
  ExternalLink
} from 'lucide-react';
import { Exam, ExamResult, IntegritySummary } from '../../types/exam';
import { examService } from '../../services/examService';
import { certificateService } from '../../services/certificateService';
import { useToast } from '../../contexts/ToastContext';
import { LoadingSpinner } from '../common/LoadingSpinner';

interface ExamResultsModalProps {
  exam: Exam;
  isOpen: boolean;
  onClose: () => void;
  onViewScorecard: (result: ExamResult) => void;
}

export const ExamResultsModal: React.FC<ExamResultsModalProps> = ({
  exam,
  isOpen,
  onClose,
  onViewScorecard,
}) => {
  const [results, setResults] = useState<ExamResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [selectedIntegrity, setSelectedIntegrity] = useState<IntegritySummary | null>(null);
  const [loadingIntegrity, setLoadingIntegrity] = useState(false);
  const [loadingScorecardId, setLoadingScorecardId] = useState<string | null>(null);
  const [issuingCertAttemptId, setIssuingCertAttemptId] = useState<string | null>(null);

  const { showToast } = useToast();

  const handleIssueCertificateForCandidate = async (attemptId: string, studentName: string) => {
    try {
      setIssuingCertAttemptId(attemptId);
      await certificateService.issueCertificate(attemptId);
      showToast(`Digital certificate issued successfully for ${studentName}!`, 'success');
    } catch (err: unknown) {
      showToast(err instanceof Error ? err.message : 'Could not issue certificate', 'error');
    } finally {
      setIssuingCertAttemptId(null);
    }
  };

  useEffect(() => {
    if (!isOpen) return;

    const loadResults = async () => {
      try {
        setLoading(true);
        const res = await examService.getExamResults(exam.id);
        setResults(res.items || []);
      } catch (err: unknown) {
        showToast(err instanceof Error ? err.message : 'Failed to load exam results', 'error');
      } finally {
        setLoading(false);
      }
    };

    loadResults();
  }, [isOpen, exam.id]);

  if (!isOpen) return null;

  const handleViewIntegrity = async (attemptId: string) => {
    try {
      setLoadingIntegrity(true);
      const summary = await examService.getAttemptIntegrity(attemptId);
      setSelectedIntegrity(summary);
    } catch (err: unknown) {
      showToast(err instanceof Error ? err.message : 'Failed to load proctoring logs', 'error');
    } finally {
      setLoadingIntegrity(false);
    }
  };

  const handleOpenScorecard = async (attemptId: string) => {
    try {
      setLoadingScorecardId(attemptId);
      const fullResult = await examService.getAttemptResult(attemptId);
      onViewScorecard(fullResult);
    } catch (err: unknown) {
      showToast(err instanceof Error ? err.message : 'Failed to load full scorecard', 'error');
    } finally {
      setLoadingScorecardId(null);
    }
  };

  const filtered = results.filter(
    (r) =>
      r.student_name.toLowerCase().includes(search.toLowerCase()) ||
      r.student_roll_number.toLowerCase().includes(search.toLowerCase())
  );

  const passCount = results.filter((r) => r.pass_fail === 'PASS').length;
  const avgPercentage =
    results.length > 0
      ? (results.reduce((acc, r) => acc + r.percentage, 0) / results.length).toFixed(1)
      : '0.0';

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-xs overflow-y-auto">
      <div className="relative w-full max-w-4xl bg-white dark:bg-zinc-900 rounded-2xl shadow-xl border border-zinc-200 dark:border-zinc-800 flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-zinc-200 dark:border-zinc-800">
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-lg font-bold text-zinc-900 dark:text-zinc-50">
                {exam.name}
              </h2>
              <span className="text-xs px-2 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 font-semibold text-zinc-600 dark:text-zinc-300">
                {exam.subject_code}
              </span>
            </div>
            <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">
              Candidate Results, Scorecards & Integrity Audit
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300 hover:bg-zinc-100 dark:bg-zinc-800"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Aggregate Stats Strip */}
        <div className="grid grid-cols-4 gap-3 p-4 bg-zinc-50 dark:bg-zinc-900/50 border-b border-zinc-200 dark:border-zinc-800 text-xs">
          <div className="p-3 bg-white dark:bg-zinc-800/80 rounded-xl border border-zinc-200 dark:border-zinc-700/60">
            <span className="text-zinc-500">Evaluated Candidates</span>
            <p className="text-lg font-bold text-zinc-900 dark:text-zinc-100 mt-0.5">
              {results.length}
            </p>
          </div>
          <div className="p-3 bg-white dark:bg-zinc-800/80 rounded-xl border border-zinc-200 dark:border-zinc-700/60">
            <span className="text-zinc-500">Pass Rate</span>
            <p className="text-lg font-bold text-emerald-600 dark:text-emerald-400 mt-0.5">
              {results.length > 0 ? `${((passCount / results.length) * 100).toFixed(0)}%` : '0%'}
            </p>
          </div>
          <div className="p-3 bg-white dark:bg-zinc-800/80 rounded-xl border border-zinc-200 dark:border-zinc-700/60">
            <span className="text-zinc-500">Average Score</span>
            <p className="text-lg font-bold text-indigo-600 dark:text-indigo-400 mt-0.5">
              {avgPercentage}%
            </p>
          </div>
          <div className="p-3 bg-white dark:bg-zinc-800/80 rounded-xl border border-zinc-200 dark:border-zinc-700/60">
            <span className="text-zinc-500">Passing Threshold</span>
            <p className="text-lg font-bold text-zinc-700 dark:text-zinc-300 mt-0.5">
              {exam.passing_percentage}%
            </p>
          </div>
        </div>

        {/* Content Table */}
        <div className="p-6 overflow-y-auto flex-1">
          <div className="flex items-center justify-between mb-4">
            <div className="relative w-72">
              <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-zinc-400" />
              <input
                type="text"
                placeholder="Search candidate by name or roll..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="w-full pl-9 pr-3 py-1.5 text-xs rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700"
              />
            </div>
          </div>

          {loading ? (
            <div className="py-16 flex justify-center">
              <LoadingSpinner size="md" />
            </div>
          ) : filtered.length === 0 ? (
            <div className="text-center py-12 text-zinc-500 text-xs">
              No evaluated candidate attempts found for this examination.
            </div>
          ) : (
            <div className="border border-zinc-200 dark:border-zinc-800 rounded-xl overflow-hidden">
              <table className="w-full text-xs text-left">
                <thead className="bg-zinc-50 dark:bg-zinc-800/60 text-zinc-600 dark:text-zinc-300 uppercase tracking-wider font-semibold border-b border-zinc-200 dark:border-zinc-800">
                  <tr>
                    <th className="py-2.5 px-4 w-12 text-center">Rank</th>
                    <th className="py-2.5 px-4">Candidate</th>
                    <th className="py-2.5 px-4">Roll No</th>
                    <th className="py-2.5 px-4 text-center">Marks</th>
                    <th className="py-2.5 px-4 text-center">% Score</th>
                    <th className="py-2.5 px-4 text-center">Grade</th>
                    <th className="py-2.5 px-4 text-center">Result</th>
                    <th className="py-2.5 px-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-200 dark:divide-zinc-800">
                  {filtered.map((r, idx) => (
                    <tr key={r.result_id} className="hover:bg-zinc-50/50 dark:hover:bg-zinc-800/40 transition-colors">
                      <td className="py-2.5 px-4 text-center font-bold text-zinc-700 dark:text-zinc-300">
                        {r.rank || idx + 1}
                      </td>
                      <td className="py-2.5 px-4 font-semibold text-zinc-900 dark:text-zinc-100">
                        {r.student_name}
                      </td>
                      <td className="py-2.5 px-4 text-zinc-500 font-mono">
                        {r.student_roll_number}
                      </td>
                      <td className="py-2.5 px-4 text-center font-medium">
                        {r.obtained_marks} / {r.total_marks}
                      </td>
                      <td className="py-2.5 px-4 text-center font-bold text-indigo-600 dark:text-indigo-400">
                        {r.percentage.toFixed(1)}%
                      </td>
                      <td className="py-2.5 px-4 text-center">
                        <span className="px-2 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 font-bold">
                          {r.grade}
                        </span>
                      </td>
                      <td className="py-2.5 px-4 text-center">
                        {r.pass_fail === 'PASS' ? (
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300">
                            <CheckCircle2 className="w-3 h-3" /> PASS
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-rose-100 text-rose-800 dark:bg-rose-900/40 dark:text-rose-300">
                            <XCircle className="w-3 h-3" /> FAIL
                          </span>
                        )}
                      </td>
                      <td className="py-2.5 px-4 text-right">
                        <div className="flex items-center justify-end gap-1.5">
                          <button
                            onClick={() => handleViewIntegrity(r.attempt_id)}
                            className="p-1 rounded text-zinc-400 hover:text-amber-600 hover:bg-zinc-100 dark:hover:bg-zinc-800"
                            title="Proctoring Integrity Audit"
                          >
                            <ShieldAlert className="w-4 h-4" />
                          </button>
                          {r.pass_fail === 'PASS' && (
                            <button
                              onClick={() => handleIssueCertificateForCandidate(r.attempt_id, r.student_name)}
                              disabled={issuingCertAttemptId === r.attempt_id}
                              className="px-2 py-1 rounded bg-amber-50 dark:bg-amber-950/40 hover:bg-amber-100 dark:hover:bg-amber-900/60 text-amber-700 dark:text-amber-300 border border-amber-200/60 dark:border-amber-800/40 font-semibold text-[11px] flex items-center gap-1 transition-colors disabled:opacity-50"
                              title="Award Digital Certificate"
                            >
                              {issuingCertAttemptId === r.attempt_id ? (
                                <LoadingSpinner size="sm" />
                              ) : (
                                <>
                                  <Award className="w-3 h-3 text-amber-600" />
                                  Issue Cert
                                </>
                              )}
                            </button>
                          )}
                          <button
                            onClick={() => handleOpenScorecard(r.attempt_id)}
                            disabled={loadingScorecardId === r.attempt_id}
                            className="px-2.5 py-1 rounded bg-zinc-100 dark:bg-zinc-800 hover:bg-zinc-200 text-zinc-700 dark:text-zinc-300 font-medium text-[11px] flex items-center gap-1 transition-colors disabled:opacity-50"
                          >
                            {loadingScorecardId === r.attempt_id ? (
                              <LoadingSpinner size="sm" />
                            ) : (
                              <>
                                Scorecard <ExternalLink className="w-3 h-3" />
                              </>
                            )}
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Proctoring Integrity Modal Overlay */}
        {selectedIntegrity && (
          <div className="fixed inset-0 z-60 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs">
            <div className="w-full max-w-lg bg-white dark:bg-zinc-900 rounded-2xl shadow-2xl border border-zinc-200 dark:border-zinc-800 p-6 space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-zinc-200 dark:border-zinc-800">
                <div className="flex items-center gap-2 text-amber-600 dark:text-amber-400 font-bold text-sm">
                  <ShieldAlert className="w-5 h-5" />
                  Proctoring Audit: {selectedIntegrity.student_name}
                </div>
                <button
                  onClick={() => setSelectedIntegrity(null)}
                  className="text-zinc-400 hover:text-zinc-600"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>

              <div className="grid grid-cols-2 gap-2 text-xs">
                <div className="p-2.5 rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700">
                  <span className="text-zinc-500">Tab Switches</span>
                  <p className="text-base font-bold text-amber-600 mt-0.5">
                    {selectedIntegrity.tab_switches}
                  </p>
                </div>
                <div className="p-2.5 rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700">
                  <span className="text-zinc-500">Window Blurs</span>
                  <p className="text-base font-bold text-amber-600 mt-0.5">
                    {selectedIntegrity.window_blurs}
                  </p>
                </div>
                <div className="p-2.5 rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700">
                  <span className="text-zinc-500">Fullscreen Exits</span>
                  <p className="text-base font-bold text-amber-600 mt-0.5">
                    {selectedIntegrity.fullscreen_exits}
                  </p>
                </div>
                <div className="p-2.5 rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700">
                  <span className="text-zinc-500">Total Integrity Flags</span>
                  <p className="text-base font-bold text-zinc-900 dark:text-zinc-100 mt-0.5">
                    {selectedIntegrity.total_events}
                  </p>
                </div>
              </div>

              <div className="space-y-1.5 max-h-48 overflow-y-auto pr-1 text-xs">
                <p className="font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                  Chronological Event Log
                </p>
                {selectedIntegrity.events.length === 0 ? (
                  <p className="text-zinc-500 text-center py-4">No suspicious events recorded. Clean attempt!</p>
                ) : (
                  selectedIntegrity.events.map((ev) => (
                    <div
                      key={ev.id}
                      className="p-2 rounded bg-zinc-50 dark:bg-zinc-800/80 border border-zinc-200 dark:border-zinc-700/60 flex items-center justify-between text-[11px]"
                    >
                      <span className="font-mono text-amber-600 uppercase font-bold">
                        {ev.event_type}
                      </span>
                      <span className="text-zinc-500">
                        {new Date(ev.timestamp).toLocaleTimeString()}
                      </span>
                    </div>
                  ))
                )}
              </div>

              <div className="pt-2 flex justify-end">
                <button
                  onClick={() => setSelectedIntegrity(null)}
                  className="px-4 py-1.5 text-xs font-semibold rounded-lg bg-zinc-900 text-white dark:bg-zinc-100 dark:text-zinc-900"
                >
                  Close Audit
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
