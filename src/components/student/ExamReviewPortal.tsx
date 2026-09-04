import React, { useState } from 'react';
import {
  Award,
  CheckCircle2,
  XCircle,
  HelpCircle,
  BarChart2,
  Clock,
  ArrowLeft,
  MessageSquare,
  Sparkles,
  ChevronDown,
  ChevronUp,
  FileText
} from 'lucide-react';

interface QuestionReviewItem {
  id: string;
  number: number;
  prompt: string;
  options: string[];
  userSelectedIndex: number;
  correctIndex: number;
  pointsEarned: number;
  maxPoints: number;
  timeSpentSeconds: number;
  explanation: string;
  difficulty: string;
  topic: string;
  classAccuracyPct: number;
}

export const ExamReviewPortal: React.FC = () => {
  const [expandedQ, setExpandedQ] = useState<number | null>(1);
  const [filterMode, setFilterMode] = useState<'ALL' | 'INCORRECT' | 'FLAGGED'>('ALL');

  const questions: QuestionReviewItem[] = [
    {
      id: 'q1',
      number: 1,
      prompt: 'What is the tight worst-case time complexity of searching for an element in a balanced Red-Black Tree containing n elements?',
      options: ['O(1)', 'O(log n)', 'O(n)', 'O(n log n)'],
      userSelectedIndex: 1,
      correctIndex: 1,
      pointsEarned: 2.0,
      maxPoints: 2.0,
      timeSpentSeconds: 42,
      explanation: 'Red-Black Trees enforce black-height balance, guaranteeing max height 2*log2(n+1), making all searches strictly O(log n).',
      difficulty: 'Intermediate',
      topic: 'Algorithms & Data Structures',
      classAccuracyPct: 78.4
    },
    {
      id: 'q2',
      number: 2,
      prompt: 'Which ANSI SQL isolation level prevents both Dirty Reads and Non-Repeatable Reads, but allows Phantom Reads?',
      options: ['Read Uncommitted', 'Read Committed', 'Repeatable Read', 'Serializable'],
      userSelectedIndex: 1,
      correctIndex: 2,
      pointsEarned: 0.0,
      maxPoints: 2.0,
      timeSpentSeconds: 68,
      explanation: 'Repeatable Read prevents dirty reads (reads of uncommitted data) and non-repeatable reads (re-reading same row gives same value), but does not prevent phantom reads (new rows inserted by concurrent transactions matching a range query). Only Serializable prevents phantom reads.',
      difficulty: 'Proficient',
      topic: 'Database Systems',
      classAccuracyPct: 46.2
    },
    {
      id: 'q3',
      number: 3,
      prompt: 'In the Raft distributed consensus protocol, which condition must be met for a node to vote YES for a candidate requesting a vote?',
      options: [
        'The candidate must be running on the node with lowest network latency',
        "The candidate's log must be at least as up-to-date as the voter's own log",
        'The candidate must have completed log compaction within the last 60 seconds',
        'The candidate must have executed more client transactions than any other replica'
      ],
      userSelectedIndex: 1,
      correctIndex: 1,
      pointsEarned: 2.0,
      maxPoints: 2.0,
      timeSpentSeconds: 54,
      explanation: 'Raft election safety requires that a voter only grant vote if the candidate has log entries as up-to-date as the receiver (evaluated by comparing latest term and index).',
      difficulty: 'Proficient',
      topic: 'Distributed Systems',
      classAccuracyPct: 62.0
    }
  ];

  const totalPointsEarned = questions.reduce((acc, q) => acc + q.pointsEarned, 0);
  const totalMaxPoints = questions.reduce((acc, q) => acc + q.maxPoints, 0);
  const scorePct = (totalPointsEarned / totalMaxPoints) * 100;

  const filteredQuestions = questions.filter((q) => {
    if (filterMode === 'INCORRECT') return q.pointsEarned === 0;
    return true;
  });

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center space-x-2 text-blue-600 dark:text-blue-400 font-semibold text-xs uppercase tracking-wider mb-1">
            <Award className="w-4 h-4" />
            <span>Candidate Examination Review</span>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Post-Assessment Feedback & Analysis
          </h2>
          <p className="text-gray-500 dark:text-gray-400 text-sm mt-1">
            CS301: Distributed Systems & Data Engineering • Final Examination (Fall 2026)
          </p>
        </div>

        <div className="flex items-center space-x-2 bg-gray-100 dark:bg-gray-700 p-1 rounded-lg text-xs font-semibold">
          <button
            onClick={() => setFilterMode('ALL')}
            className={`px-3 py-1.5 rounded-md transition-all ${
              filterMode === 'ALL'
                ? 'bg-white dark:bg-gray-800 text-blue-600 dark:text-blue-400 shadow-sm'
                : 'text-gray-600 dark:text-gray-300'
            }`}
          >
            All Items ({questions.length})
          </button>
          <button
            onClick={() => setFilterMode('INCORRECT')}
            className={`px-3 py-1.5 rounded-md transition-all ${
              filterMode === 'INCORRECT'
                ? 'bg-white dark:bg-gray-800 text-blue-600 dark:text-blue-400 shadow-sm'
                : 'text-gray-600 dark:text-gray-300'
            }`}
          >
            Incorrect Only ({questions.filter((q) => q.pointsEarned === 0).length})
          </button>
        </div>
      </div>

      {/* Summary Scorecard */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="p-5 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
          <span className="text-xs uppercase font-bold text-gray-400">Total Score</span>
          <div className="text-3xl font-black text-gray-900 dark:text-white font-mono my-1">
            {totalPointsEarned.toFixed(1)} <span className="text-base text-gray-400">/ {totalMaxPoints.toFixed(1)}</span>
          </div>
          <span className="text-xs font-bold text-blue-600">{scorePct.toFixed(1)}% Marks</span>
        </div>

        <div className="p-5 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
          <span className="text-xs uppercase font-bold text-gray-400">Grade Letter</span>
          <div className="text-3xl font-black text-emerald-600 font-mono my-1">A-</div>
          <span className="text-xs text-gray-500">Passing Grade: PASS</span>
        </div>

        <div className="p-5 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
          <span className="text-xs uppercase font-bold text-gray-400">Class Percentile</span>
          <div className="text-3xl font-black text-purple-600 font-mono my-1">84.2%</div>
          <span className="text-xs text-gray-500">Above average cohort performance</span>
        </div>

        <div className="p-5 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
          <span className="text-xs uppercase font-bold text-gray-400">Time Consumed</span>
          <div className="text-3xl font-black text-gray-900 dark:text-white font-mono my-1">48m 22s</div>
          <span className="text-xs text-gray-500">Time limit: 90 minutes</span>
        </div>
      </div>

      {/* Item-by-Item Review Accordion */}
      <div className="space-y-4">
        {filteredQuestions.map((q) => {
          const isExpanded = expandedQ === q.number;
          const isCorrect = q.pointsEarned === q.maxPoints;

          return (
            <div
              key={q.id}
              className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm overflow-hidden"
            >
              <div
                onClick={() => setExpandedQ(isExpanded ? null : q.number)}
                className="p-5 flex justify-between items-center cursor-pointer hover:bg-gray-50/60 dark:hover:bg-gray-700/20 transition-colors"
              >
                <div className="flex items-center space-x-3">
                  {isCorrect ? (
                    <div className="w-8 h-8 rounded-full bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300 flex items-center justify-center shrink-0">
                      <CheckCircle2 className="w-5 h-5" />
                    </div>
                  ) : (
                    <div className="w-8 h-8 rounded-full bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-300 flex items-center justify-center shrink-0">
                      <XCircle className="w-5 h-5" />
                    </div>
                  )}

                  <div>
                    <div className="flex items-center space-x-2">
                      <span className="text-xs font-bold text-gray-400">Question #{q.number}</span>
                      <span className="text-xs px-2 py-0.5 rounded bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 font-medium">
                        {q.topic}
                      </span>
                    </div>
                    <h4 className="text-sm font-semibold text-gray-900 dark:text-white line-clamp-1 mt-0.5">
                      {q.prompt}
                    </h4>
                  </div>
                </div>

                <div className="flex items-center space-x-6 text-xs shrink-0">
                  <span className="font-mono font-bold text-gray-700 dark:text-gray-300">
                    {q.pointsEarned.toFixed(1)} / {q.maxPoints.toFixed(1)} pts
                  </span>
                  {isExpanded ? <ChevronUp className="w-4 h-4 text-gray-400" /> : <ChevronDown className="w-4 h-4 text-gray-400" />}
                </div>
              </div>

              {isExpanded && (
                <div className="p-5 pt-0 border-t border-gray-100 dark:border-gray-700 space-y-4 mt-2">
                  <div className="text-sm text-gray-800 dark:text-gray-200 leading-relaxed font-medium">
                    {q.prompt}
                  </div>

                  <div className="space-y-2">
                    {q.options.map((opt, optIdx) => {
                      const isUserChoice = q.userSelectedIndex === optIdx;
                      const isRightChoice = q.correctIndex === optIdx;

                      let badgeClass = 'border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-300';
                      if (isRightChoice) {
                        badgeClass = 'border-green-500 bg-green-50 dark:bg-green-950/30 text-green-950 dark:text-green-100 font-semibold';
                      } else if (isUserChoice && !isRightChoice) {
                        badgeClass = 'border-red-500 bg-red-50 dark:bg-red-950/30 text-red-950 dark:text-red-100 font-semibold';
                      }

                      return (
                        <div
                          key={optIdx}
                          className={`p-3 rounded-lg border text-xs flex justify-between items-center ${badgeClass}`}
                        >
                          <div className="flex items-center space-x-2">
                            <span className="font-bold">{String.fromCharCode(65 + optIdx)}.</span>
                            <span>{opt}</span>
                          </div>

                          <div>
                            {isRightChoice && (
                              <span className="text-[10px] uppercase font-bold text-green-700 dark:text-green-300 px-2 py-0.5 rounded bg-green-100 dark:bg-green-900/40">
                                Correct Answer
                              </span>
                            )}
                            {isUserChoice && !isRightChoice && (
                              <span className="text-[10px] uppercase font-bold text-red-700 dark:text-red-300 px-2 py-0.5 rounded bg-red-100 dark:bg-red-900/40">
                                Your Choice
                              </span>
                            )}
                          </div>
                        </div>
                      );
                    })}
                  </div>

                  {/* Explanation Box */}
                  <div className="p-4 bg-blue-50/60 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-800 rounded-xl space-y-1 text-xs">
                    <span className="font-bold text-blue-900 dark:text-blue-200 block uppercase text-[10px] tracking-wider">
                      Authoritative Explanation
                    </span>
                    <p className="text-blue-900 dark:text-blue-100 leading-relaxed">
                      {q.explanation}
                    </p>
                  </div>

                  <div className="flex justify-between items-center text-xs text-gray-500 pt-2 border-t border-gray-100 dark:border-gray-700">
                    <div className="flex items-center space-x-4">
                      <span>Time spent: <strong>{q.timeSpentSeconds}s</strong></span>
                      <span>Class accuracy: <strong>{q.classAccuracyPct}%</strong></span>
                    </div>

                    <button className="inline-flex items-center space-x-1 text-gray-500 hover:text-blue-600 font-medium">
                      <MessageSquare className="w-3.5 h-3.5" />
                      <span>Request Faculty Re-evaluation</span>
                    </button>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
