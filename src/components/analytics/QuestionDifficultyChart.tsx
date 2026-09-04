/**
 * ExamHub - Question Psychometric Matrix Component
 * Displays facility index (P) and item discrimination (D) per question.
 */

import React from 'react';
import { QuestionItemMetric } from '../../types/analytics';

interface QuestionDifficultyChartProps {
  metrics: QuestionItemMetric[];
}

export const QuestionDifficultyChart: React.FC<QuestionDifficultyChartProps> = ({ metrics }) => {
  return (
    <div className="bg-white dark:bg-zinc-900 p-5 rounded-2xl border border-zinc-200 dark:border-zinc-800 shadow-xs space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-bold text-zinc-900 dark:text-zinc-100">
            Item Psychometric Matrix (Classical Test Theory)
          </h3>
          <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">
            Facility Index (P-value) vs. Item Discrimination (Kelley&apos;s 27% Rule)
          </p>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs">
          <thead>
            <tr className="border-b border-zinc-200 dark:border-zinc-800 text-zinc-400 uppercase font-semibold">
              <th className="py-2 px-3">#</th>
              <th className="py-2 px-3">Question Text</th>
              <th className="py-2 px-3">Topic</th>
              <th className="py-2 px-3">Facility (P)</th>
              <th className="py-2 px-3">Discrim (D)</th>
              <th className="py-2 px-3">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-100 dark:divide-zinc-800">
            {metrics.map((q) => {
              const pPct = Math.round(q.facility_index * 100);

              let statusColor = 'bg-zinc-100 text-zinc-700 dark:bg-zinc-800 dark:text-zinc-300';
              if (q.discrimination_status === 'Excellent') {
                statusColor = 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950/40 dark:text-emerald-300 font-bold';
              } else if (q.discrimination_status === 'Good') {
                statusColor = 'bg-blue-100 text-blue-800 dark:bg-blue-950/40 dark:text-blue-300 font-medium';
              } else if (q.discrimination_status === 'Marginal') {
                statusColor = 'bg-amber-100 text-amber-800 dark:bg-amber-950/40 dark:text-amber-300';
              } else if (q.discrimination_status === 'Defective') {
                statusColor = 'bg-rose-100 text-rose-800 dark:bg-rose-950/40 dark:text-rose-300 font-bold';
              }

              return (
                <tr key={q.question_id} className="hover:bg-zinc-50 dark:hover:bg-zinc-800/50 transition-colors">
                  <td className="py-2.5 px-3 font-bold text-zinc-500">Q{q.order_index}</td>
                  <td className="py-2.5 px-3 font-medium text-zinc-800 dark:text-zinc-200 max-w-xs truncate">
                    {q.question_text}
                  </td>
                  <td className="py-2.5 px-3 text-zinc-500">{q.topic || 'General'}</td>
                  <td className="py-2.5 px-3">
                    <div className="flex items-center gap-2">
                      <div className="w-16 h-2 rounded-full bg-zinc-200 dark:bg-zinc-700 overflow-hidden">
                        <div
                          style={{ width: `${pPct}%` }}
                          className={`h-full ${pPct >= 60 ? 'bg-emerald-500' : pPct >= 30 ? 'bg-amber-500' : 'bg-rose-500'}`}
                        />
                      </div>
                      <span className="font-mono text-[11px]">{pPct}%</span>
                    </div>
                  </td>
                  <td className="py-2.5 px-3 font-mono font-bold text-zinc-700 dark:text-zinc-300">
                    {q.discrimination_index >= 0 ? `+${q.discrimination_index}` : q.discrimination_index}
                  </td>
                  <td className="py-2.5 px-3">
                    <span className={`px-2 py-0.5 rounded-full text-[10px] ${statusColor}`}>
                      {q.discrimination_status}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};
