/**
 * ExamHub - Metric Stat Card Component
 */

import React from 'react';

interface StatCardProps {
  label: string;
  value: string | number;
  subtext?: string;
  icon?: React.ReactNode;
  variant?: 'default' | 'success' | 'warning' | 'danger' | 'info';
}

export const StatCard: React.FC<StatCardProps> = ({
  label,
  value,
  subtext,
  icon,
  variant = 'default',
}) => {
  const variantStyles = {
    default: 'bg-white dark:bg-zinc-900 border-zinc-200 dark:border-zinc-800 text-zinc-900 dark:text-zinc-100',
    success: 'bg-emerald-50/50 dark:bg-emerald-950/20 border-emerald-200/60 dark:border-emerald-800/40 text-emerald-900 dark:text-emerald-100',
    warning: 'bg-amber-50/50 dark:bg-amber-950/20 border-amber-200/60 dark:border-amber-800/40 text-amber-900 dark:text-amber-100',
    danger: 'bg-rose-50/50 dark:bg-rose-950/20 border-rose-200/60 dark:border-rose-800/40 text-rose-900 dark:text-rose-100',
    info: 'bg-indigo-50/50 dark:bg-indigo-950/20 border-indigo-200/60 dark:border-indigo-800/40 text-indigo-900 dark:text-indigo-100',
  };

  return (
    <div className={`p-5 rounded-2xl border shadow-xs transition-all ${variantStyles[variant]}`}>
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold uppercase tracking-wider text-zinc-500 dark:text-zinc-400">
          {label}
        </span>
        {icon && <div className="p-2 rounded-xl bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-300">{icon}</div>}
      </div>
      <div className="text-2xl font-black mt-2 tracking-tight">
        {value}
      </div>
      {subtext && (
        <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">
          {subtext}
        </p>
      )}
    </div>
  );
};
