/**
 * ExamHub - Comprehensive Post-Exam Scorecard & Solution Review
 */

import React, { useState } from 'react';
import {
  Award,
  CheckCircle2,
  XCircle,
  Clock,
  ArrowLeft,
  BookOpen,
  ChevronDown,
  ChevronUp,
  Share2,
  Printer
} from 'lucide-react';
import { ExamResult } from '../../types/exam';

interface ExamResultScorecardProps {
  result: ExamResult;
  onBack: () => void;
}

export const ExamResultScorecard: React.FC<ExamResultScorecardProps> = ({
  result,
  onBack,
}) => {
  const [filterDifficulty, setFilterDifficulty] = useState<string>('all');
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);

  const isPass = result.pass_fail === 'PASS';

  const filteredItems = result.review_items.filter((item) => {
    if (filterDifficulty === 'all') return true;
    if (filterDifficulty === 'correct') return item.is_correct;
    if (filterDifficulty === 'wrong') return !item.is_correct && item.selected_option !== null;
    if (filterDifficulty === 'unanswered') return item.selected_option === null;
    return true;
  });

  return (
    <div id="exam-scorecard-container" className="max-w-4xl mx-auto space-y-6 pb-12">
      {/* Top Action Bar */}
      <div className="flex items-center justify-between">
        <button
          onClick={onBack}
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-100"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Portal
        </button>
        <button
          onClick={() => window.print()}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-lg border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-700 dark:text-zinc-200 hover:bg-zinc-50"
        >
          <Printer className="w-3.5 h-3.5" />
          Print Scorecard
        </button>
      </div>

      {/* Main Scorecard Hero Card */}
      <div className="bg-white dark:bg-zinc-900 rounded-3xl border border-zinc-200 dark:border-zinc-800 p-6 sm:p-8 shadow-sm relative overflow-hidden">
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs font-bold px-2.5 py-0.5 rounded bg-indigo-50 text-indigo-700 dark:bg-indigo-950/40 dark:text-indigo-300">
                {result.subject_code}
              </span>
              <span className="text-xs text-zinc-500 font-medium">
                {result.subject_name}
              </span>
            </div>
            <h1 className="text-2xl font-black text-zinc-900 dark:text-zinc-50 tracking-tight">
              {result.exam_name}
            </h1>
            <p className="text-xs text-zinc-500 mt-1">
              Candidate: <strong className="text-zinc-800 dark:text-zinc-200">{result.student_name}</strong> • Roll: {result.student_roll_number}
            </p>
          </div>

          {/* Result Badge & Percentage */}
          <div className="flex items-center gap-5">
            <div className="text-center">
              <span className="text-xs text-zinc-400 font-semibold block uppercase tracking-wider">
                Score
              </span>
              <div className="text-3xl font-black text-zinc-900 dark:text-zinc-100 mt-0.5">
                {result.obtained_marks}{' '}
                <span className="text-sm font-normal text-zinc-400">/ {result.total_marks}</span>
              </div>
            </div>

            <div className="h-12 w-px bg-zinc-200 dark:bg-zinc-800" />

            <div className="text-center">
              <span className="text-xs text-zinc-400 font-semibold block uppercase tracking-wider">
                Grade
              </span>
              <div className="text-3xl font-black text-indigo-600 dark:text-indigo-400 mt-0.5">
                {result.grade}
              </div>
            </div>

            <div className="h-12 w-px bg-zinc-200 dark:bg-zinc-800" />

            <div>
              {isPass ? (
                <div className="px-4 py-2 rounded-2xl bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300 font-black text-sm uppercase tracking-wider flex items-center gap-1.5">
                  <CheckCircle2 className="w-5 h-5" /> PASS
                </div>
              ) : (
                <div className="px-4 py-2 rounded-2xl bg-rose-100 text-rose-800 dark:bg-rose-950/60 dark:text-rose-300 font-black text-sm uppercase tracking-wider flex items-center gap-1.5">
                  <XCircle className="w-5 h-5" /> FAIL
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Aggregate Stats Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-8 pt-6 border-t border-zinc-100 dark:border-zinc-800 text-xs">
          <div className="p-3.5 rounded-2xl bg-zinc-50 dark:bg-zinc-800/40 border border-zinc-200 dark:border-zinc-700/60">
            <span className="text-zinc-500 font-medium">Percentage</span>
            <p className="text-xl font-bold text-zinc-900 dark:text-zinc-100 mt-1">
              {result.percentage.toFixed(1)}%
            </p>
          </div>
          <div className="p-3.5 rounded-2xl bg-emerald-50 dark:bg-emerald-950/20 border border-emerald-200/50 dark:border-emerald-800/30">
            <span className="text-emerald-700 dark:text-emerald-300 font-medium">Correct Answers</span>
            <p className="text-xl font-bold text-emerald-700 dark:text-emerald-300 mt-1">
              {result.correct_count} / {result.total_questions}
            </p>
          </div>
          <div className="p-3.5 rounded-2xl bg-rose-50 dark:bg-rose-950/20 border border-rose-200/50 dark:border-rose-800/30">
            <span className="text-rose-700 dark:text-rose-300 font-medium">Incorrect Answers</span>
            <p className="text-xl font-bold text-rose-700 dark:text-rose-300 mt-1">
              {result.wrong_count}
            </p>
          </div>
          <div className="p-3.5 rounded-2xl bg-indigo-50 dark:bg-indigo-950/20 border border-indigo-200/50 dark:border-indigo-800/30">
            <span className="text-indigo-700 dark:text-indigo-300 font-medium">Candidate Rank</span>
            <p className="text-xl font-bold text-indigo-700 dark:text-indigo-300 mt-1">
              #{result.rank || 1}{' '}
              <span className="text-xs font-normal text-zinc-500">of {result.total_candidates}</span>
            </p>
          </div>
        </div>
      </div>

      {/* Solutions & Explanation Section */}
      <div className="bg-white dark:bg-zinc-900 rounded-3xl border border-zinc-200 dark:border-zinc-800 p-6 sm:p-8 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-5 border-b border-zinc-100 dark:border-zinc-800">
          <div>
            <h2 className="text-lg font-bold text-zinc-900 dark:text-zinc-50">
              Detailed Question Analysis & Explanations
            </h2>
            <p className="text-xs text-zinc-500 mt-0.5">
              Review your submitted answers alongside verified correct answers and pedagogical explanations.
            </p>
          </div>

          {/* Filter Pills */}
          <div className="flex items-center gap-1.5 text-xs bg-zinc-100 dark:bg-zinc-800 p-1 rounded-xl">
            {(
              [
                { key: 'all', label: 'All' },
                { key: 'correct', label: 'Correct' },
                { key: 'wrong', label: 'Incorrect' },
                { key: 'unanswered', label: 'Skipped' },
              ] as const
            ).map((tab) => (
              <button
                key={tab.key}
                onClick={() => setFilterDifficulty(tab.key)}
                className={`px-3 py-1 rounded-lg font-medium transition-all ${
                  filterDifficulty === tab.key
                    ? 'bg-white dark:bg-zinc-900 text-zinc-900 dark:text-zinc-100 shadow-xs font-semibold'
                    : 'text-zinc-600 dark:text-zinc-400 hover:text-zinc-900'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Questions Accordion / List */}
        <div className="space-y-4 mt-6">
          {filteredItems.map((item, idx) => {
            const isExpanded = expandedIndex === idx;
            return (
              <div
                key={item.question_id}
                className={`rounded-2xl border transition-all ${
                  item.is_correct
                    ? 'border-emerald-200/80 dark:border-emerald-900/40 bg-emerald-50/20 dark:bg-emerald-950/10'
                    : item.selected_option
                    ? 'border-rose-200/80 dark:border-rose-900/40 bg-rose-50/20 dark:bg-rose-950/10'
                    : 'border-zinc-200 dark:border-zinc-800 bg-zinc-50/40 dark:bg-zinc-900/40'
                }`}
              >
                <div
                  onClick={() => setExpandedIndex(isExpanded ? null : idx)}
                  className="p-4 sm:p-5 flex items-start justify-between gap-4 cursor-pointer"
                >
                  <div className="flex items-start gap-3">
                    <div className="mt-0.5">
                      {item.is_correct ? (
                        <CheckCircle2 className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
                      ) : (
                        <XCircle className="w-5 h-5 text-rose-600 dark:text-rose-400" />
                      )}
                    </div>
                    <div>
                      <div className="flex items-center gap-2 text-xs mb-1">
                        <span className="font-bold text-zinc-500">Q{idx + 1}</span>
                        <span className="px-1.5 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 text-[10px] font-medium text-zinc-600">
                          {item.difficulty}
                        </span>
                        {item.topic && (
                          <span className="text-[11px] text-zinc-400">• {item.topic}</span>
                        )}
                      </div>
                      <p className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">
                        {item.question_text}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-3 shrink-0">
                    <span className="text-xs font-bold text-zinc-700 dark:text-zinc-300">
                      {item.marks_obtained} / {item.marks_allocated} Marks
                    </span>
                    {isExpanded ? (
                      <ChevronUp className="w-4 h-4 text-zinc-400" />
                    ) : (
                      <ChevronDown className="w-4 h-4 text-zinc-400" />
                    )}
                  </div>
                </div>

                {/* Expanded Content with Option Comparison and Explanation */}
                {isExpanded && (
                  <div className="px-5 pb-5 pt-1 border-t border-zinc-100 dark:border-zinc-800 text-xs space-y-3">
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mt-2">
                      {(['A', 'B', 'C', 'D'] as const).map((opt) => {
                        const optText = item[`option_${opt.toLowerCase()}` as keyof typeof item] as string;
                        const isSelected = item.selected_option === opt;
                        const isCorrect = item.correct_answer === opt;

                        let badgeStyle = 'bg-zinc-50 dark:bg-zinc-800 border-zinc-200 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300';
                        if (isCorrect) {
                          badgeStyle = 'bg-emerald-100 dark:bg-emerald-950/60 border-emerald-400 text-emerald-900 dark:text-emerald-200 font-bold';
                        } else if (isSelected) {
                          badgeStyle = 'bg-rose-100 dark:bg-rose-950/60 border-rose-400 text-rose-900 dark:text-rose-200 font-bold';
                        }

                        return (
                          <div
                            key={opt}
                            className={`p-2.5 rounded-xl border flex items-center gap-2 ${badgeStyle}`}
                          >
                            <span className="w-5 h-5 rounded-full bg-white dark:bg-zinc-900 border flex items-center justify-center font-bold text-[10px]">
                              {opt}
                            </span>
                            <span className="flex-1">{optText}</span>
                            {isCorrect && (
                              <span className="text-[10px] uppercase font-bold text-emerald-700 dark:text-emerald-300">
                                Correct
                              </span>
                            )}
                            {isSelected && !isCorrect && (
                              <span className="text-[10px] uppercase font-bold text-rose-700 dark:text-rose-300">
                                Selected
                              </span>
                            )}
                          </div>
                        );
                      })}
                    </div>

                    {item.explanation && (
                      <div className="mt-3 p-3 rounded-xl bg-indigo-50/70 dark:bg-indigo-950/30 border border-indigo-100 dark:border-indigo-900/50">
                        <span className="font-bold text-indigo-900 dark:text-indigo-300 block mb-0.5">
                          Pedagogical Explanation:
                        </span>
                        <p className="text-zinc-700 dark:text-zinc-300 leading-relaxed">
                          {item.explanation}
                        </p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
