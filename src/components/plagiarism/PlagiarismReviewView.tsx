import React, { useState } from 'react';
import {
  FileSearch,
  AlertTriangle,
  CheckCircle2,
  Users,
  GitCompare,
  ExternalLink,
  ShieldAlert,
  Search,
  Sparkles
} from 'lucide-react';

interface CollusionPair {
  candidateA: string;
  candidateB: string;
  similarityPct: number;
  sharedFingerprints: number;
  timeDiffSeconds: number;
  ipMatch: boolean;
  verdict: string;
}

export const PlagiarismReviewView: React.FC = () => {
  const [similarityThreshold, setSimilarityThreshold] = useState<number>(40);
  const [selectedPair, setSelectedPair] = useState<CollusionPair | null>({
    candidateA: 'STU_101 (Alex Vance)',
    candidateB: 'STU_102 (Gordon Freeman)',
    similarityPct: 88.4,
    sharedFingerprints: 42,
    timeDiffSeconds: 15,
    ipMatch: true,
    verdict: 'Severe Collusion / Direct Plagiarism'
  });

  const pairs: CollusionPair[] = [
    {
      candidateA: 'STU_101 (Alex Vance)',
      candidateB: 'STU_102 (Gordon Freeman)',
      similarityPct: 88.4,
      sharedFingerprints: 42,
      timeDiffSeconds: 15,
      ipMatch: true,
      verdict: 'Severe Collusion / Direct Plagiarism'
    },
    {
      candidateA: 'STU_104 (Alyx Smith)',
      candidateB: 'STU_109 (Barney Calhoun)',
      similarityPct: 54.2,
      sharedFingerprints: 24,
      timeDiffSeconds: 140,
      ipMatch: false,
      verdict: 'Suspicious Substantial Overlap'
    },
    {
      candidateA: 'STU_112 (Eli Vance)',
      candidateB: 'STU_118 (Isaac Kleiner)',
      similarityPct: 38.0,
      sharedFingerprints: 16,
      timeDiffSeconds: 320,
      ipMatch: false,
      verdict: 'Moderate Similarity (Common Template)'
    }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center space-x-2 text-rose-600 dark:text-rose-400 font-semibold text-xs uppercase tracking-wider mb-1">
            <FileSearch className="w-4 h-4" />
            <span>Academic Integrity & Winnowing Fingerprints</span>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Plagiarism & Cohort Collusion Auditor
          </h2>
          <p className="text-gray-500 dark:text-gray-400 text-sm mt-1">
            Identifies unauthorized candidate collaboration using Schleimer winnowing hashes and IP subnet matching.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2 bg-gray-100 dark:bg-gray-700 px-3 py-1.5 rounded-lg text-xs">
            <span className="text-gray-500 font-medium">Threshold:</span>
            <span className="font-bold text-gray-800 dark:text-gray-200 font-mono">{similarityThreshold}%</span>
            <input
              type="range"
              min="20"
              max="90"
              value={similarityThreshold}
              onChange={(e) => setSimilarityThreshold(parseInt(e.target.value))}
              className="w-24 accent-rose-600"
            />
          </div>
        </div>
      </div>

      {/* Flagged Pairs Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="bg-white dark:bg-gray-800 p-5 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm space-y-4">
          <h3 className="text-sm font-bold text-gray-900 dark:text-white uppercase tracking-wider flex items-center space-x-1.5">
            <ShieldAlert className="w-4 h-4 text-rose-500" />
            <span>Flagged Submission Pairs ({pairs.length})</span>
          </h3>

          <div className="space-y-2.5">
            {pairs.map((p, idx) => (
              <div
                key={idx}
                onClick={() => setSelectedPair(p)}
                className={`p-3.5 rounded-xl border transition-all cursor-pointer ${
                  selectedPair?.candidateA === p.candidateA
                    ? 'border-rose-500 bg-rose-50/60 dark:bg-rose-950/30 ring-1 ring-rose-500'
                    : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600 bg-white dark:bg-gray-800'
                }`}
              >
                <div className="flex justify-between items-center mb-1">
                  <span className="text-xs font-bold text-gray-900 dark:text-white truncate max-w-[170px]">
                    {p.candidateA.split(' ')[0]} ⇄ {p.candidateB.split(' ')[0]}
                  </span>
                  <span
                    className={`text-xs font-black font-mono px-2 py-0.5 rounded ${
                      p.similarityPct >= 80
                        ? 'bg-rose-100 text-rose-700 dark:bg-rose-900/40 dark:text-rose-300'
                        : p.similarityPct >= 50
                        ? 'bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300'
                        : 'bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300'
                    }`}
                  >
                    {p.similarityPct.toFixed(1)}%
                  </span>
                </div>
                <div className="text-[11px] text-gray-500 flex justify-between items-center mt-1">
                  <span>{p.sharedFingerprints} shared hashes</span>
                  {p.ipMatch && (
                    <span className="text-red-600 dark:text-red-400 font-bold">Same IP Subnet</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Side-by-side comparison inspector */}
        <div className="lg:col-span-2 bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm space-y-6">
          {selectedPair ? (
            <>
              <div className="flex justify-between items-start pb-4 border-b border-gray-100 dark:border-gray-700">
                <div>
                  <div className="flex items-center space-x-2">
                    <GitCompare className="w-5 h-5 text-rose-600" />
                    <h3 className="text-base font-bold text-gray-900 dark:text-white">
                      Collusion Differential Inspection
                    </h3>
                  </div>
                  <p className="text-xs text-rose-600 dark:text-rose-400 font-semibold mt-1">
                    {selectedPair.verdict} • Submitted within {selectedPair.timeDiffSeconds} seconds
                  </p>
                </div>

                <div className="text-right">
                  <span className="text-2xl font-black text-rose-600 font-mono">
                    {selectedPair.similarityPct.toFixed(1)}%
                  </span>
                  <span className="text-[10px] text-gray-400 block">Jaccard Fingerprint Index</span>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <div className="flex justify-between items-center text-xs font-bold text-gray-700 dark:text-gray-300">
                    <span>{selectedPair.candidateA}</span>
                    <span className="text-gray-400 font-mono">IP: 192.168.1.50</span>
                  </div>
                  <div className="p-4 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50 text-xs font-serif leading-relaxed text-gray-800 dark:text-gray-200 h-64 overflow-y-auto">
                    <span className="bg-rose-100 dark:bg-rose-900/40 text-rose-950 dark:text-rose-200 p-0.5 rounded">
                      Distributed consensus algorithms ensure fault tolerance across unreliable network partitions
                    </span>{' '}
                    using state machine replication and quorum elections. When a leader node receives a client write,
                    it appends the entry to its local log and propagates append RPC messages to followers.
                  </div>
                </div>

                <div className="space-y-2">
                  <div className="flex justify-between items-center text-xs font-bold text-gray-700 dark:text-gray-300">
                    <span>{selectedPair.candidateB}</span>
                    <span className="text-gray-400 font-mono">IP: 192.168.1.50</span>
                  </div>
                  <div className="p-4 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50 text-xs font-serif leading-relaxed text-gray-800 dark:text-gray-200 h-64 overflow-y-auto">
                    <span className="bg-rose-100 dark:bg-rose-900/40 text-rose-950 dark:text-rose-200 p-0.5 rounded">
                      Distributed consensus algorithms ensure fault tolerance across unreliable network partitions
                    </span>{' '}
                    using state machine replication and quorum votes. When a primary receives a client transaction, it
                    records the entry to its disk log and propagates log append calls to replicas.
                  </div>
                </div>
              </div>

              <div className="flex justify-between items-center pt-2 border-t border-gray-100 dark:border-gray-700">
                <span className="text-xs text-gray-500">
                  Schleimer winnowing algorithm: 25-gram characters with 15-gram sliding window minimum.
                </span>
                <div className="flex space-x-2">
                  <button className="px-3 py-1.5 rounded-lg border border-gray-200 dark:border-gray-700 text-xs font-semibold hover:bg-gray-50">
                    Dismiss Match
                  </button>
                  <button className="px-4 py-1.5 bg-rose-600 hover:bg-rose-700 text-white rounded-lg text-xs font-semibold shadow-sm">
                    Escalate to Academic Honor Board
                  </button>
                </div>
              </div>
            </>
          ) : (
            <div className="text-center py-20 text-gray-400 text-xs">
              Select a flagged pair from the left column to view detailed text overlap.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
