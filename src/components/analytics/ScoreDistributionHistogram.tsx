/**
 * ExamHub - Score Distribution Histogram Component
 * Visualizes score distribution across deciles with interactive SVG bars.
 */

import React from 'react';
import { DecileDistribution } from '../../types/analytics';

interface ScoreDistributionHistogramProps {
  deciles: DecileDistribution[];
  passingScore?: number;
}

export const ScoreDistributionHistogram: React.FC<ScoreDistributionHistogramProps> = ({
  deciles,
}) => {
  const maxCount = Math.max(1, ...deciles.map((d) => d.student_count));

  return (
    <div className="bg-white dark:bg-zinc-900 p-5 rounded-2xl border border-zinc-200 dark:border-zinc-800 shadow-xs">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-bold text-zinc-900 dark:text-zinc-100">
            Score Distribution (Deciles)
          </h3>
          <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">
            Cohort frequency across score percentage intervals
          </p>
        </div>
      </div>

      <div className="h-44 flex items-end gap-2 pt-4 pb-2 border-b border-zinc-200 dark:border-zinc-800">
        {deciles.map((d) => {
          const heightPercent = (d.student_count / maxCount) * 100;
          const isPassing = d.lower_bound >= 40;

          return (
            <div key={d.decile} className="flex-1 flex flex-col items-center h-full justify-end group relative">
              {/* Tooltip on Hover */}
              <div className="absolute -top-8 bg-zinc-900 text-white text-[10px] px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-20 shadow-md">
                {d.decile}: {d.student_count} student(s) ({d.percentage_of_cohort}%)
              </div>

              <div
                style={{ height: `${Math.max(6, heightPercent)}%` }}
                className={`w-full rounded-t-lg transition-all duration-300 ${
                  isPassing
                    ? 'bg-indigo-500 hover:bg-indigo-600 dark:bg-indigo-600 dark:hover:bg-indigo-500'
                    : 'bg-rose-400 hover:bg-rose-500 dark:bg-rose-600 dark:hover:bg-rose-500'
                }`}
              />
            </div>
          );
        })}
      </div>

      <div className="flex justify-between mt-2 text-[10px] text-zinc-400 font-mono">
        <span>0%</span>
        <span>20%</span>
        <span>40% (Pass)</span>
        <span>60%</span>
        <span>80%</span>
        <span>100%</span>
      </div>
    </div>
  );
};
