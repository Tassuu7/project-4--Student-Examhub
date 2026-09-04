import React, { useState } from 'react';
import {
  BookOpen,
  Layers,
  CheckCircle2,
  AlertCircle,
  BarChart3,
  Sparkles,
  ChevronRight,
  Filter,
  Plus,
  Compass
} from 'lucide-react';

interface Competency {
  code: string;
  title: string;
  level: string; // Remember, Understand, Apply, Analyze, Evaluate, Create
  weight: number;
  coveragePct: number;
  status: 'COVERED' | 'PARTIAL' | 'DEFICIT';
}

interface ModuleBlueprint {
  moduleCode: string;
  moduleTitle: string;
  totalCredits: number;
  overallCoverage: number;
  competencies: Competency[];
}

export const CurriculumBlueprintView: React.FC = () => {
  const [selectedModule, setSelectedModule] = useState<string>('CS201');

  const blueprints: ModuleBlueprint[] = [
    {
      moduleCode: 'CS201',
      moduleTitle: 'Algorithms & Data Structures',
      totalCredits: 4.0,
      overallCoverage: 87.5,
      competencies: [
        { code: 'CS-ALG-1.1', title: 'Asymptotic Complexity & Recurrence Relations', level: 'ANALYZE', weight: 25, coveragePct: 92.0, status: 'COVERED' },
        { code: 'CS-ALG-1.2', title: 'Self-Balancing Binary Search Trees (AVL/Red-Black)', level: 'APPLY', weight: 25, coveragePct: 88.0, status: 'COVERED' },
        { code: 'CS-ALG-1.3', title: 'Graph Traversal & Shortest Paths (Dijkstra/Bellman-Ford)', level: 'EVALUATE', weight: 25, coveragePct: 85.0, status: 'COVERED' },
        { code: 'CS-ALG-1.4', title: 'Dynamic Programming & Memoization Optimization', level: 'CREATE', weight: 25, coveragePct: 62.0, status: 'PARTIAL' }
      ]
    },
    {
      moduleCode: 'CS301',
      moduleTitle: 'Distributed Cloud Computing & Fault Tolerance',
      totalCredits: 4.0,
      overallCoverage: 91.0,
      competencies: [
        { code: 'CS-DIST-2.1', title: 'CAP Theorem & Multi-Region Consistency Models', level: 'ANALYZE', weight: 30, coveragePct: 95.0, status: 'COVERED' },
        { code: 'CS-DIST-2.2', title: 'Distributed Consensus Protocols (Raft/Paxos)', level: 'EVALUATE', weight: 40, coveragePct: 90.0, status: 'COVERED' },
        { code: 'CS-DIST-2.3', title: 'Atomic Commitment & Two-Phase Locking', level: 'CREATE', weight: 30, coveragePct: 88.0, status: 'COVERED' }
      ]
    },
    {
      moduleCode: 'CS401',
      moduleTitle: 'Applied Cryptography & Network Security',
      totalCredits: 4.0,
      overallCoverage: 74.0,
      competencies: [
        { code: 'CS-SEC-3.1', title: 'Symmetric Block Ciphers & AES-GCM Modes', level: 'ANALYZE', weight: 30, coveragePct: 84.0, status: 'COVERED' },
        { code: 'CS-SEC-3.2', title: 'Asymmetric Cryptography & Elliptic Curves (ECDSA)', level: 'EVALUATE', weight: 40, coveragePct: 78.0, status: 'COVERED' },
        { code: 'CS-SEC-3.3', title: 'Public Key Infrastructure & TLS 1.3 Handshake', level: 'APPLY', weight: 30, coveragePct: 58.0, status: 'DEFICIT' }
      ]
    }
  ];

  const currentBlueprint = blueprints.find((b) => b.moduleCode === selectedModule) || blueprints[0];

  const bloomsLevels = [
    { label: 'Remember', color: 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300', count: 12 },
    { label: 'Understand', color: 'bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300', count: 24 },
    { label: 'Apply', color: 'bg-teal-100 text-teal-700 dark:bg-teal-900/40 dark:text-teal-300', count: 35 },
    { label: 'Analyze', color: 'bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300', count: 28 },
    { label: 'Evaluate', color: 'bg-purple-100 text-purple-700 dark:bg-purple-900/40 dark:text-purple-300', count: 18 },
    { label: 'Create', color: 'bg-rose-100 text-rose-700 dark:bg-rose-900/40 dark:text-rose-300', count: 8 }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center space-x-2 text-violet-600 dark:text-violet-400 font-semibold text-xs uppercase tracking-wider mb-1">
            <Compass className="w-4 h-4" />
            <span>Curriculum Engineering & Standards Alignment</span>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Curriculum Blueprint & Bloom's Taxonomy Matrix
          </h2>
          <p className="text-gray-500 dark:text-gray-400 text-sm mt-1">
            Map test items to cognitive complexity dimensions and identify curriculum coverage gaps.
          </p>
        </div>

        <div className="flex items-center space-x-2">
          {blueprints.map((bp) => (
            <button
              key={bp.moduleCode}
              onClick={() => setSelectedModule(bp.moduleCode)}
              className={`px-3.5 py-2 rounded-lg text-xs font-semibold transition-all ${
                selectedModule === bp.moduleCode
                  ? 'bg-violet-600 text-white shadow-sm'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              {bp.moduleCode} ({bp.overallCoverage}%)
            </button>
          ))}
        </div>
      </div>

      {/* Bloom's Cognitive Distribution Strip */}
      <div className="bg-white dark:bg-gray-800 p-5 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
        <h4 className="text-xs uppercase font-bold text-gray-500 dark:text-gray-400 mb-3 tracking-wider">
          Cognitive Complexity Distribution (Bloom's Revised Taxonomy)
        </h4>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          {bloomsLevels.map((lvl) => (
            <div
              key={lvl.label}
              className={`p-3 rounded-lg border border-transparent font-medium text-xs text-center ${lvl.color}`}
            >
              <div className="text-lg font-black font-mono">{lvl.count} Items</div>
              <div className="text-[11px] opacity-90 uppercase tracking-wide">{lvl.label}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Module Competencies List */}
      <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm space-y-4">
        <div className="flex justify-between items-center pb-2 border-b border-gray-100 dark:border-gray-700">
          <div>
            <h3 className="text-base font-bold text-gray-900 dark:text-white">
              {currentBlueprint.moduleCode} — {currentBlueprint.moduleTitle}
            </h3>
            <span className="text-xs text-gray-500">Academic Credits: {currentBlueprint.totalCredits.toFixed(1)}</span>
          </div>

          <div className="text-right">
            <span className="text-xs text-gray-400 block">Overall Blueprint Coverage</span>
            <span className="text-lg font-bold font-mono text-violet-600 dark:text-violet-400">
              {currentBlueprint.overallCoverage.toFixed(1)}%
            </span>
          </div>
        </div>

        <div className="space-y-3">
          {currentBlueprint.competencies.map((comp) => (
            <div
              key={comp.code}
              className="p-4 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50/50 dark:bg-gray-900/30 flex flex-col md:flex-row justify-between items-start md:items-center gap-4 hover:border-violet-300 dark:hover:border-violet-700 transition-colors"
            >
              <div className="space-y-1 max-w-xl">
                <div className="flex items-center space-x-2">
                  <span className="font-mono text-xs font-bold text-violet-600 dark:text-violet-400">
                    {comp.code}
                  </span>
                  <span className="text-xs px-2 py-0.5 rounded bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold uppercase text-[10px]">
                    {comp.level}
                  </span>
                </div>
                <h4 className="text-sm font-semibold text-gray-900 dark:text-white">
                  {comp.title}
                </h4>
              </div>

              <div className="flex items-center space-x-6 shrink-0 w-full md:w-auto justify-between md:justify-end">
                <div className="text-right">
                  <span className="text-[11px] text-gray-400 block">Item Bank Coverage</span>
                  <span className="text-sm font-bold font-mono text-gray-900 dark:text-white">
                    {comp.coveragePct.toFixed(1)}%
                  </span>
                </div>

                <div className="w-24 bg-gray-200 dark:bg-gray-700 h-2 rounded-full overflow-hidden">
                  <div
                    className={`h-full ${
                      comp.status === 'COVERED' ? 'bg-green-500' : comp.status === 'PARTIAL' ? 'bg-amber-500' : 'bg-red-500'
                    }`}
                    style={{ width: `${comp.coveragePct}%` }}
                  />
                </div>

                <div>
                  {comp.status === 'COVERED' && (
                    <span className="inline-flex items-center space-x-1 px-2.5 py-1 bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300 rounded text-xs font-bold">
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      <span>OPTIMAL</span>
                    </span>
                  )}
                  {comp.status === 'PARTIAL' && (
                    <span className="inline-flex items-center space-x-1 px-2.5 py-1 bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300 rounded text-xs font-bold">
                      <AlertCircle className="w-3.5 h-3.5" />
                      <span>PARTIAL</span>
                    </span>
                  )}
                  {comp.status === 'DEFICIT' && (
                    <span className="inline-flex items-center space-x-1 px-2.5 py-1 bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300 rounded text-xs font-bold">
                      <AlertCircle className="w-3.5 h-3.5" />
                      <span>DEFICIT</span>
                    </span>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
