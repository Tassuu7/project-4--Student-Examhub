import React, { useState } from 'react';
import {
  BarChart3,
  TrendingUp,
  PieChart,
  Users,
  Layers,
  Download,
  AlertTriangle,
  ArrowUpRight,
  ArrowDownRight,
  Filter,
  CheckCircle2
} from 'lucide-react';

export const ComprehensiveAnalyticsView: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'item_curves' | 'cohort_clusters' | 'score_scaling' | 'item_drift'>('item_curves');

  const items = [
    { id: 'Q1', p: 0.78, d: 0.42, rpb: 0.48, status: 'EXCELLENT', domain: 'Algorithms' },
    { id: 'Q2', p: 0.46, d: 0.52, rpb: 0.54, status: 'EXCELLENT', domain: 'Databases' },
    { id: 'Q3', p: 0.89, d: 0.18, rpb: 0.22, status: 'TOO_EASY', domain: 'Operating Systems' },
    { id: 'Q4', p: 0.32, d: 0.38, rpb: 0.41, status: 'CHALLENGING', domain: 'Distributed Systems' },
    { id: 'Q5', p: 0.18, d: -0.05, rpb: -0.12, status: 'DEFECTIVE_KEY', domain: 'Cryptography' }
  ];

  const clusters = [
    { name: 'Fast Masters', count: 18, pct: '28%', meanScore: '91.4%', speed: '32s/item', profile: 'High accuracy with rapid execution' },
    { name: 'Methodical Solvers', count: 32, pct: '50%', meanScore: '78.2%', speed: '74s/item', profile: 'Steady deliberate pacing, strong verification' },
    { name: 'Struggling Guessers', count: 14, pct: '22%', meanScore: '42.6%', speed: '21s/item', profile: 'Low dwell times, erratic guessing patterns' }
  ];

  const stanineBands = [
    { stanine: 9, range: 'Z ≥ +1.75', pct: '4%', count: 3, label: 'Very Superior' },
    { stanine: 8, range: '+1.25 to +1.75', pct: '7%', count: 5, label: 'Superior' },
    { stanine: 7, range: '+0.75 to +1.25', pct: '12%', count: 8, label: 'High Average' },
    { stanine: 6, range: '+0.25 to +0.75', pct: '17%', count: 11, label: 'Slightly Above Average' },
    { stanine: 5, range: '-0.25 to +0.25', pct: '20%', count: 13, label: 'Average' },
    { stanine: 4, range: '-0.75 to -0.25', pct: '17%', count: 11, label: 'Slightly Below Average' },
    { stanine: 3, range: '-1.25 to -0.75', pct: '12%', count: 8, label: 'Low Average' },
    { stanine: 2, range: '-1.75 to -1.25', pct: '7%', count: 4, label: 'Poor' },
    { stanine: 1, range: 'Z < -1.75', pct: '4%', count: 1, label: 'Very Poor' }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center space-x-2 text-indigo-600 dark:text-indigo-400 font-semibold text-xs uppercase tracking-wider mb-1">
            <BarChart3 className="w-4 h-4" />
            <span>Psychometric Measurement Laboratory</span>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Advanced Examination Analytics & Psychometrics
          </h2>
          <p className="text-gray-500 dark:text-gray-400 text-sm mt-1">
            Classical test theory, Rasch item characteristic curves, stanine normalizations, and candidate archetype clustering.
          </p>
        </div>

        <div className="flex bg-gray-100 dark:bg-gray-700 p-1 rounded-lg text-xs font-semibold">
          <button
            onClick={() => setActiveTab('item_curves')}
            className={`px-3 py-1.5 rounded-md transition-all ${
              activeTab === 'item_curves'
                ? 'bg-white dark:bg-gray-800 text-indigo-600 dark:text-indigo-400 shadow-sm'
                : 'text-gray-600 dark:text-gray-300'
            }`}
          >
            Item Psychometrics
          </button>
          <button
            onClick={() => setActiveTab('cohort_clusters')}
            className={`px-3 py-1.5 rounded-md transition-all ${
              activeTab === 'cohort_clusters'
                ? 'bg-white dark:bg-gray-800 text-indigo-600 dark:text-indigo-400 shadow-sm'
                : 'text-gray-600 dark:text-gray-300'
            }`}
          >
            Candidate Clusters
          </button>
          <button
            onClick={() => setActiveTab('score_scaling')}
            className={`px-3 py-1.5 rounded-md transition-all ${
              activeTab === 'score_scaling'
                ? 'bg-white dark:bg-gray-800 text-indigo-600 dark:text-indigo-400 shadow-sm'
                : 'text-gray-600 dark:text-gray-300'
            }`}
          >
            Stanine Normalization
          </button>
          <button
            onClick={() => setActiveTab('item_drift')}
            className={`px-3 py-1.5 rounded-md transition-all ${
              activeTab === 'item_drift'
                ? 'bg-white dark:bg-gray-800 text-indigo-600 dark:text-indigo-400 shadow-sm'
                : 'text-gray-600 dark:text-gray-300'
            }`}
          >
            Parameter Drift
          </button>
        </div>
      </div>

      {activeTab === 'item_curves' && (
        <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm space-y-4">
          <h3 className="text-sm font-bold text-gray-900 dark:text-white uppercase tracking-wider">
            Item Difficulty (P) & Discrimination (D) Matrix
          </h3>

          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left">
              <thead className="bg-gray-50 dark:bg-gray-700/50 text-gray-500 font-semibold uppercase">
                <tr>
                  <th className="py-2.5 px-3">Item ID</th>
                  <th className="py-2.5 px-3">Curricular Domain</th>
                  <th className="py-2.5 px-3 text-center">Facility P-Value</th>
                  <th className="py-2.5 px-3 text-center">Discrimination (Kelley's D)</th>
                  <th className="py-2.5 px-3 text-center">Point-Biserial (r_pbis)</th>
                  <th className="py-2.5 px-3 text-center">Quality Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
                {items.map((it) => (
                  <tr key={it.id} className="hover:bg-gray-50/50 dark:hover:bg-gray-700/20">
                    <td className="py-3 px-3 font-bold font-mono text-gray-800 dark:text-gray-200">{it.id}</td>
                    <td className="py-3 px-3 text-gray-700 dark:text-gray-300">{it.domain}</td>
                    <td className="py-3 px-3 text-center font-mono font-semibold">{it.p.toFixed(2)}</td>
                    <td className="py-3 px-3 text-center font-mono font-semibold text-indigo-600 dark:text-indigo-400">
                      {it.d >= 0 ? `+${it.d.toFixed(2)}` : it.d.toFixed(2)}
                    </td>
                    <td className="py-3 px-3 text-center font-mono">{it.rpb.toFixed(2)}</td>
                    <td className="py-3 px-3 text-center">
                      <span
                        className={`px-2.5 py-0.5 rounded text-[10px] font-bold ${
                          it.status === 'EXCELLENT'
                            ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300'
                            : it.status === 'DEFECTIVE_KEY'
                            ? 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300'
                            : 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300'
                        }`}
                      >
                        {it.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {activeTab === 'cohort_clusters' && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {clusters.map((c, i) => (
            <div
              key={i}
              className="p-6 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm space-y-3"
            >
              <div className="flex justify-between items-center">
                <span className="text-xs font-bold text-indigo-600 dark:text-indigo-400 uppercase">
                  Archetype #{i + 1}
                </span>
                <span className="text-xs font-bold text-gray-400 font-mono">{c.pct}</span>
              </div>
              <h4 className="text-lg font-bold text-gray-900 dark:text-white">{c.name}</h4>
              <p className="text-xs text-gray-500 leading-relaxed">{c.profile}</p>

              <div className="pt-3 border-t border-gray-100 dark:border-gray-700 space-y-1.5 text-xs text-gray-600 dark:text-gray-300">
                <div className="flex justify-between">
                  <span>Candidate Count:</span>
                  <span className="font-bold font-mono">{c.count} students</span>
                </div>
                <div className="flex justify-between">
                  <span>Mean Exam Score:</span>
                  <span className="font-bold font-mono text-green-600">{c.meanScore}</span>
                </div>
                <div className="flex justify-between">
                  <span>Response Pacing:</span>
                  <span className="font-bold font-mono">{c.speed}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {activeTab === 'score_scaling' && (
        <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm space-y-4">
          <h3 className="text-sm font-bold text-gray-900 dark:text-white uppercase tracking-wider">
            Stanine Normal Distribution Curve
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-3 lg:grid-cols-9 gap-2">
            {stanineBands.map((s) => (
              <div
                key={s.stanine}
                className="p-3 bg-gray-50 dark:bg-gray-900/40 rounded-xl border border-gray-200 dark:border-gray-700 text-center space-y-1"
              >
                <div className="text-xs font-bold text-indigo-600 dark:text-indigo-400">Band {s.stanine}</div>
                <div className="text-xl font-black font-mono text-gray-900 dark:text-white">{s.count}</div>
                <div className="text-[10px] text-gray-400">{s.pct}</div>
                <div className="text-[10px] text-gray-500 truncate" title={s.label}>
                  {s.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'item_drift' && (
        <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm space-y-4">
          <h3 className="text-sm font-bold text-gray-900 dark:text-white uppercase tracking-wider">
            Longitudinal Item Parameter Drift (IPD) Tracker
          </h3>
          <div className="p-4 bg-amber-50 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-800 rounded-xl text-xs flex items-start space-x-3">
            <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
            <div>
              <div className="font-bold text-amber-900 dark:text-amber-200">
                Item #Q42 Shift Detected: Difficulty parameter dropped by Δb = -0.68 logits
              </div>
              <p className="text-amber-800/80 dark:text-amber-300/80 mt-1">
                Facility rose from P = 0.52 (Fall 2024) to P = 0.81 (Spring 2026). Statistical anomaly exceeds drift threshold (0.35). Recommended action: Retire question due to possible question bank compromise.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
