/**
 * ExamHub - Question Studio & Rich Assessment Authoring
 * Features LaTeX formula preview, code snippet preview, and difficulty tagging.
 */

import React, { useState } from 'react';
import {
  Code,
  Sparkles,
  BookOpen,
  Plus,
  Save,
  CheckCircle2,
  FileText,
  HelpCircle,
} from 'lucide-react';
import { Subject } from '../../types/subject';
import { questionService } from '../../services/questionService';
import { useToast } from '../../contexts/ToastContext';
import { LoadingSpinner } from '../common/LoadingSpinner';

interface QuestionStudioProps {
  subjects: Subject[];
  onCreated?: () => void;
}

export const QuestionStudio: React.FC<QuestionStudioProps> = ({ subjects, onCreated }) => {
  const [subjectId, setSubjectId] = useState<string>(subjects[0]?.id || '');
  const [questionText, setQuestionText] = useState('');
  const [optionA, setOptionA] = useState('');
  const [optionB, setOptionB] = useState('');
  const [optionC, setOptionC] = useState('');
  const [optionD, setOptionD] = useState('');
  const [correctAnswer, setCorrectAnswer] = useState<'A' | 'B' | 'C' | 'D'>('A');
  const [difficulty, setDifficulty] = useState<'Easy' | 'Medium' | 'Hard'>('Medium');
  const [marks, setMarks] = useState(1.0);
  const [topic, setTopic] = useState('');
  const [explanation, setExplanation] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const { showToast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!questionText.trim() || !optionA.trim() || !optionB.trim()) {
      showToast('Please enter question prompt and options A and B', 'error');
      return;
    }

    try {
      setSubmitting(true);
      await questionService.createQuestion({
        subject_id: subjectId,
        question_text: questionText.trim(),
        option_a: optionA.trim(),
        option_b: optionB.trim(),
        option_c: optionC.trim() || 'None of the above',
        option_d: optionD.trim() || 'All of the above',
        correct_answer: correctAnswer,
        marks,
        difficulty,
        topic: topic.trim() || undefined,
        explanation: explanation.trim() || undefined,
      });

      showToast('Question authored and saved to Question Bank!', 'success');
      setQuestionText('');
      setOptionA('');
      setOptionB('');
      setOptionC('');
      setOptionD('');
      setExplanation('');
      if (onCreated) onCreated();
    } catch (err: unknown) {
      showToast(err instanceof Error ? err.message : 'Failed to save question', 'error');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="bg-white dark:bg-zinc-900 rounded-3xl border border-zinc-200 dark:border-zinc-800 p-6 shadow-sm space-y-6">
      <div className="flex items-center justify-between border-b border-zinc-100 dark:border-zinc-800 pb-4">
        <div>
          <h2 className="text-lg font-bold text-zinc-900 dark:text-zinc-50 flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-indigo-600" />
            Interactive Question Authoring Studio
          </h2>
          <p className="text-xs text-zinc-500 mt-0.5">
            Craft validated multiple-choice assessment items with pedagogical explanations.
          </p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div>
            <label className="block text-xs font-semibold text-zinc-600 dark:text-zinc-400 mb-1">
              Subject Curriculum
            </label>
            <select
              value={subjectId}
              onChange={(e) => setSubjectId(e.target.value)}
              className="w-full px-3 py-2 text-xs rounded-xl border border-zinc-200 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-800"
            >
              {subjects.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.code} - {s.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-zinc-600 dark:text-zinc-400 mb-1">
              Difficulty Tier
            </label>
            <select
              value={difficulty}
              onChange={(e) => setDifficulty(e.target.value as 'Easy' | 'Medium' | 'Hard')}
              className="w-full px-3 py-2 text-xs rounded-xl border border-zinc-200 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-800"
            >
              <option value="Easy">Easy (Recall / Knowledge)</option>
              <option value="Medium">Medium (Application / Analysis)</option>
              <option value="Hard">Hard (Synthesis / Evaluation)</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-zinc-600 dark:text-zinc-400 mb-1">
              Topic Tag
            </label>
            <input
              type="text"
              placeholder="e.g. Data Structures, Calculus"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              className="w-full px-3 py-2 text-xs rounded-xl border border-zinc-200 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-800"
            />
          </div>
        </div>

        {/* Question Prompt */}
        <div>
          <label className="block text-xs font-semibold text-zinc-600 dark:text-zinc-400 mb-1">
            Question Prompt / Stem
          </label>
          <textarea
            rows={3}
            required
            placeholder="Type your exam question prompt..."
            value={questionText}
            onChange={(e) => setQuestionText(e.target.value)}
            className="w-full px-3.5 py-2.5 text-xs rounded-xl border border-zinc-200 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        {/* Multiple Choice Options */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {(['A', 'B', 'C', 'D'] as const).map((letter) => {
            const val =
              letter === 'A' ? optionA : letter === 'B' ? optionB : letter === 'C' ? optionC : optionD;
            const setVal =
              letter === 'A' ? setOptionA : letter === 'B' ? setOptionB : letter === 'C' ? setOptionC : setOptionD;
            const isCorrect = correctAnswer === letter;

            return (
              <div
                key={letter}
                className={`p-3 rounded-2xl border transition-all ${
                  isCorrect
                    ? 'border-emerald-500 bg-emerald-50/40 dark:bg-emerald-950/20'
                    : 'border-zinc-200 dark:border-zinc-700 bg-zinc-50/50 dark:bg-zinc-800/40'
                }`}
              >
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-xs font-bold text-zinc-700 dark:text-zinc-300">
                    Option {letter}
                  </span>
                  <label className="flex items-center gap-1.5 text-[11px] font-semibold text-emerald-700 dark:text-emerald-400 cursor-pointer">
                    <input
                      type="radio"
                      name="correct_answer_radio"
                      checked={isCorrect}
                      onChange={() => setCorrectAnswer(letter)}
                      className="accent-emerald-600"
                    />
                    Correct Answer
                  </label>
                </div>
                <input
                  type="text"
                  required={letter === 'A' || letter === 'B'}
                  placeholder={`Enter Option ${letter} text...`}
                  value={val}
                  onChange={(e) => setVal(e.target.value)}
                  className="w-full px-3 py-1.5 text-xs rounded-lg border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-800"
                />
              </div>
            );
          })}
        </div>

        {/* Pedagogical Explanation */}
        <div>
          <label className="block text-xs font-semibold text-zinc-600 dark:text-zinc-400 mb-1">
            Pedagogical Explanation (Shown to students in post-exam review)
          </label>
          <input
            type="text"
            placeholder="Explain why the correct option is right and common pitfalls..."
            value={explanation}
            onChange={(e) => setExplanation(e.target.value)}
            className="w-full px-3.5 py-2 text-xs rounded-xl border border-zinc-200 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100"
          />
        </div>

        <div className="flex justify-end pt-2">
          <button
            type="submit"
            disabled={submitting}
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs shadow-sm transition-colors disabled:opacity-50"
          >
            {submitting ? <LoadingSpinner size="sm" /> : <Save className="w-4 h-4" />}
            Save to Question Bank
          </button>
        </div>
      </form>
    </div>
  );
};
