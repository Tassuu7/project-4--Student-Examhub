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

  const { showToast } = useToast();

  const loadFeed = async () => {
    try {
      const data = await proctoringService.getLiveFeed();
      setFeed(data);
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

        {/* Right: Selected Candidate Detailed Telemetry Timeline */}
        <div className="lg:col-span-5 bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 p-5 shadow-xs">
          <h3 className="text-sm font-bold text-zinc-900 dark:text-zinc-100 mb-3">
            Candidate Integrity Audit
          </h3>

          {loadingProfile ? (
            <div className="py-12 flex justify-center">
              <LoadingSpinner size="md" />
            </div>
          ) : !candidateProfile ? (
            <div className="py-12 text-center text-zinc-400 text-xs">
              Select a candidate from the roster to view their live telemetry timeline.
            </div>
          ) : (
            <div className="space-y-4">
              {/* Profile Summary Badge */}
              <div
                className={`p-4 rounded-xl border ${
                  candidateProfile.risk_level === 'Severe' || candidateProfile.risk_level === 'High'
                    ? 'border-rose-200 bg-rose-50/50 dark:bg-rose-950/20 text-rose-900 dark:text-rose-100'
                    : 'border-emerald-200 bg-emerald-50/50 dark:bg-emerald-950/20 text-emerald-900 dark:text-emerald-100'
                }`}
              >
                <div className="flex justify-between items-center">
                  <span className="text-xs font-bold uppercase tracking-wider">
                    Risk Assessment: {candidateProfile.risk_level}
                  </span>
                  <span className="font-mono font-black text-lg">
                    {candidateProfile.integrity_score}/100
                  </span>
                </div>
                <div className="grid grid-cols-2 gap-2 mt-2 pt-2 border-t border-current/20 text-[11px]">
                  <div>Tab Switches: <strong>{candidateProfile.tab_switch_count}</strong></div>
                  <div>Focus Loss: <strong>{candidateProfile.blur_count}</strong></div>
                </div>
              </div>

              {/* Event Log Stream */}
              <div className="space-y-2 max-h-72 overflow-y-auto pr-1">
                <h4 className="text-[11px] uppercase font-bold text-zinc-400">
                  Telemetry Event Stream ({candidateProfile.events.length})
                </h4>
                {candidateProfile.events.length === 0 ? (
                  <p className="text-xs text-zinc-400 py-4 text-center">
                    Clean session. No suspicious behavior recorded.
                  </p>
                ) : (
                  candidateProfile.events.map((ev) => (
                    <div
                      key={ev.id}
                      className="p-2.5 rounded-lg border border-zinc-100 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-800/40 text-xs flex justify-between items-start gap-2"
                    >
                      <div>
                        <span className="font-bold text-zinc-800 dark:text-zinc-200 block">
                          {ev.event_type}
                        </span>
                        <p className="text-[11px] text-zinc-500">{ev.details}</p>
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
    </div>
  );
};
