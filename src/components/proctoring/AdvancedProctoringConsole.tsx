import React, { useState } from 'react';
import {
  ShieldAlert,
  Video,
  Mic,
  Eye,
  AlertTriangle,
  CheckCircle2,
  Users,
  Search,
  Filter,
  Maximize2,
  Monitor,
  Sparkles,
  PhoneOff,
  Radio
} from 'lucide-react';

interface CandidateFeed {
  id: string;
  name: string;
  exam: string;
  status: 'NORMAL' | 'WARNING' | 'CRITICAL';
  trustScore: number;
  warningsCount: number;
  lastAnomaly: string;
  audioNoiseLevelDb: number;
  headYaw: number;
}

export const AdvancedProctoringConsole: React.FC = () => {
  const [selectedCandidate, setSelectedCandidate] = useState<CandidateFeed | null>(null);
  const [filterSeverity, setFilterSeverity] = useState<'ALL' | 'WARNINGS_ONLY'>('ALL');

  const candidates: CandidateFeed[] = [
    {
      id: 'cand-101',
      name: 'Alex Vance',
      exam: 'CS301 Final',
      status: 'NORMAL',
      trustScore: 96,
      warningsCount: 0,
      lastAnomaly: 'None',
      audioNoiseLevelDb: 28,
      headYaw: 3.2
    },
    {
      id: 'cand-102',
      name: 'Gordon Freeman',
      exam: 'CS301 Final',
      status: 'WARNING',
      trustScore: 68,
      warningsCount: 2,
      lastAnomaly: 'Window focus lost for 4.2 seconds',
      audioNoiseLevelDb: 34,
      headYaw: 14.5
    },
    {
      id: 'cand-103',
      name: 'Alyx Smith',
      exam: 'CS301 Final',
      status: 'CRITICAL',
      trustScore: 32,
      warningsCount: 5,
      lastAnomaly: 'Multiple human faces detected in webcam frame',
      audioNoiseLevelDb: 58,
      headYaw: 28.0
    },
    {
      id: 'cand-104',
      name: 'Barney Calhoun',
      exam: 'CS301 Final',
      status: 'NORMAL',
      trustScore: 92,
      warningsCount: 1,
      lastAnomaly: 'Minor audio whisper detected',
      audioNoiseLevelDb: 31,
      headYaw: 4.1
    }
  ];

  const displayedCandidates = candidates.filter((c) => {
    if (filterSeverity === 'WARNINGS_ONLY') return c.status !== 'NORMAL';
    return true;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center space-x-2 text-rose-600 dark:text-rose-400 font-semibold text-xs uppercase tracking-wider mb-1">
            <Radio className="w-4 h-4 text-rose-500 animate-pulse" />
            <span>Real-Time Invigilation & AI Anomaly Detection</span>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Advanced Live Proctoring Command Console
          </h2>
          <p className="text-gray-500 dark:text-gray-400 text-sm mt-1">
            Real-time biometric gaze tracking, acoustic whisper detection, multi-display boundaries, and incident escalation.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={() => setFilterSeverity(filterSeverity === 'ALL' ? 'WARNINGS_ONLY' : 'ALL')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
              filterSeverity === 'WARNINGS_ONLY'
                ? 'border-rose-500 bg-rose-50 text-rose-700 dark:bg-rose-950/40 dark:text-rose-300'
                : 'border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-300'
            }`}
          >
            {filterSeverity === 'WARNINGS_ONLY' ? 'Showing Anomalies Only' : 'Show All Feeds'}
          </button>
        </div>
      </div>

      {/* Grid of Candidate Video Tiles */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {displayedCandidates.map((c) => (
          <div
            key={c.id}
            onClick={() => setSelectedCandidate(c)}
            className={`bg-white dark:bg-gray-800 rounded-xl border p-4 shadow-sm cursor-pointer transition-all hover:shadow-md ${
              c.status === 'CRITICAL'
                ? 'border-rose-500 ring-1 ring-rose-500'
                : c.status === 'WARNING'
                ? 'border-amber-400'
                : 'border-gray-200 dark:border-gray-700 hover:border-gray-300'
            }`}
          >
            {/* Mock Webcam Preview Window */}
            <div className="w-full h-36 bg-gray-900 rounded-lg relative overflow-hidden flex items-center justify-center mb-3">
              <div className="text-gray-500 text-xs flex flex-col items-center space-y-1">
                <Video className="w-8 h-8 opacity-40" />
                <span>Webcam Stream 720p</span>
              </div>

              {/* Status Badge Over Video */}
              <div className="absolute top-2 left-2">
                <span
                  className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${
                    c.status === 'CRITICAL'
                      ? 'bg-rose-600 text-white'
                      : c.status === 'WARNING'
                      ? 'bg-amber-500 text-white'
                      : 'bg-green-600 text-white'
                  }`}
                >
                  {c.status}
                </span>
              </div>

              <div className="absolute bottom-2 right-2 bg-black/60 px-2 py-0.5 rounded text-[10px] text-white font-mono">
                {c.audioNoiseLevelDb} dB
              </div>
            </div>

            <div className="flex justify-between items-start">
              <div>
                <h4 className="text-sm font-bold text-gray-900 dark:text-white">{c.name}</h4>
                <span className="text-[11px] text-gray-400">{c.exam}</span>
              </div>
              <div className="text-right">
                <span className="text-xs font-mono font-black text-gray-900 dark:text-white">
                  {c.trustScore}%
                </span>
                <span className="text-[10px] text-gray-400 block">Trust Index</span>
              </div>
            </div>

            {c.status !== 'NORMAL' && (
              <div className="mt-2 pt-2 border-t border-gray-100 dark:border-gray-700 text-[11px] text-amber-600 dark:text-amber-400 flex items-center space-x-1 truncate">
                <AlertTriangle className="w-3.5 h-3.5 shrink-0" />
                <span className="truncate">{c.lastAnomaly}</span>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Detail Inspector Drawer */}
      {selectedCandidate && (
        <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm space-y-4">
          <div className="flex justify-between items-center pb-3 border-b border-gray-100 dark:border-gray-700">
            <div>
              <h3 className="text-base font-bold text-gray-900 dark:text-white">
                Detailed Telemetry Inspection: {selectedCandidate.name} ({selectedCandidate.id})
              </h3>
              <p className="text-xs text-gray-500 mt-0.5">Session: CS301-PROCTOR-LIVE • Stream Latency: 120ms</p>
            </div>

            <button
              onClick={() => setSelectedCandidate(null)}
              className="text-xs text-gray-400 hover:text-gray-600 font-semibold"
            >
              Close Inspector
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs">
            <div className="p-3 bg-gray-50 dark:bg-gray-900/40 rounded-lg">
              <span className="text-gray-400 block text-[11px]">Integrity Score</span>
              <span className="text-lg font-bold font-mono text-gray-900 dark:text-white">
                {selectedCandidate.trustScore}%
              </span>
            </div>
            <div className="p-3 bg-gray-50 dark:bg-gray-900/40 rounded-lg">
              <span className="text-gray-400 block text-[11px]">Head Pose Yaw Angle</span>
              <span className="text-lg font-bold font-mono text-gray-900 dark:text-white">
                {selectedCandidate.headYaw}° (Threshold: 30°)
              </span>
            </div>
            <div className="p-3 bg-gray-50 dark:bg-gray-900/40 rounded-lg">
              <span className="text-gray-400 block text-[11px]">Ambient Acoustic Noise</span>
              <span className="text-lg font-bold font-mono text-gray-900 dark:text-white">
                {selectedCandidate.audioNoiseLevelDb} dB SPL
              </span>
            </div>
            <div className="p-3 bg-gray-50 dark:bg-gray-900/40 rounded-lg">
              <span className="text-gray-400 block text-[11px]">Security Incidents</span>
              <span className="text-lg font-bold font-mono text-rose-600">
                {selectedCandidate.warningsCount} Infractions
              </span>
            </div>
          </div>

          <div className="flex justify-end space-x-3 pt-2">
            <button className="px-4 py-2 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 text-xs font-semibold rounded-lg">
              Broadcast Audio Warning to Candidate
            </button>
            <button className="px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white text-xs font-semibold rounded-lg shadow-sm">
              Pause Candidate Exam Session
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
