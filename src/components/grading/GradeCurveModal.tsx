/**
 * ExamHub - Grade Curve & Normalization Modal
 * Allows teachers to apply Square Root Curve, Linear Offset, or Bell Curve adjustments.
 */

import React, { useState } from 'react';
import { Sparkles, X, CheckCircle2 } from 'lucide-react';
import { gradingService } from '../../services/gradingService';
import { useToast } from '../../contexts/ToastContext';
import { LoadingSpinner } from '../common/LoadingSpinner';

interface GradeCurveModalProps {
  examId: string;
  examName: string;
  isOpen: boolean;
  onClose: () => void;
  onCurveApplied?: () => void;
}

export const GradeCurveModal: React.FC<GradeCurveModalProps> = ({
  examId,
  examName,
  isOpen,
  onClose,
  onCurveApplied,
}) => {
  const [method, setMethod] = useState<'linear_offset' | 'square_root' | 'bell_curve'>('linear_offset');
  const [targetMean, setTargetMean] = useState(75);
  const [loading, setLoading] = useState(false);
  const { showToast } = useToast();

  if (!isOpen) return null;

  const handleApply = async () => {
    try {
      setLoading(true);
      const res = await gradingService.applyCurve(examId, method, targetMean);
      showToast(
        `Curve applied to ${res.adjusted_scores_count} candidate(s)! Mean shifted from ${res.original_mean}% to ${res.curved_mean}%.`,
        'success'
      );
      if (onCurveApplied) onCurveApplied();
      onClose();
    } catch (err: unknown) {
      showToast(err instanceof Error ? err.message : 'Curve application failed', 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs">
      <div className="w-full max-w-md bg-white dark:bg-zinc-900 rounded-3xl shadow-2xl border border-zinc-200 dark:border-zinc-800 p-6 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-indigo-600" />
            <h2 className="text-base font-bold text-zinc-900 dark:text-zinc-50">
              Apply Score Curve
            </h2>
          </div>
          <button onClick={onClose} className="p-1 text-zinc-400 hover:text-zinc-600">
            <X className="w-4 h-4" />
          </button>
        </div>

        <p className="text-xs text-zinc-500">
          Transform scores for <strong className="text-zinc-800 dark:text-zinc-200">{examName}</strong> using statistical scaling models.
        </p>

        <div className="space-y-3 pt-2 text-xs">
          <div>
            <label className="font-semibold text-zinc-700 dark:text-zinc-300 block mb-1">
              Curving Algorithm
            </label>
            <select
              value={method}
              onChange={(e) => setMethod(e.target.value as any)}
              className="w-full px-3 py-2 rounded-xl border border-zinc-200 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-800"
            >
              <option value="linear_offset">Linear Offset (Shift to Target Mean)</option>
              <option value="square_root">Square Root Scaling (Classic sqrt(Raw) * 10)</option>
              <option value="bell_curve">Standardized Z-Score (Normal Bell Curve)</option>
            </select>
          </div>

          {method === 'linear_offset' && (
            <div>
              <label className="font-semibold text-zinc-700 dark:text-zinc-300 block mb-1">
                Target Cohort Mean Percentage ({targetMean}%)
              </label>
              <input
                type="range"
                min={50}
                max={90}
                value={targetMean}
                onChange={(e) => setTargetMean(Number(e.target.value))}
                className="w-full accent-indigo-600"
              />
            </div>
          )}
        </div>

        <div className="flex justify-end gap-2 pt-4 border-t border-zinc-100 dark:border-zinc-800">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 text-xs font-semibold rounded-xl text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800"
          >
            Cancel
          </button>
          <button
            type="button"
            disabled={loading}
            onClick={handleApply}
            className="px-4 py-2 text-xs font-semibold rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white shadow-sm transition-colors flex items-center gap-1.5"
          >
            {loading ? <LoadingSpinner size="sm" /> : <CheckCircle2 className="w-4 h-4" />}
            Apply Transformation
          </button>
        </div>
      </div>
    </div>
  );
};
