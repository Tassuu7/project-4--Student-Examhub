/**
 * ExamHub - Automated Exam Generator Modal
 * Samples questions from the Question Bank based on difficulty distribution.
 */

import React, { useState, useEffect, useId } from 'react';
import { X, Wand2, Sparkles, Sliders, CheckCircle2 } from 'lucide-react';
import { Subject } from '../../types/subject';
import { examService } from '../../services/examService';
import { SubjectService } from '../../services/subjectService';
import { useToast } from '../../contexts/ToastContext';
import { LoadingSpinner } from '../common/LoadingSpinner';

interface ExamAutoGenerateModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export const ExamAutoGenerateModal: React.FC<ExamAutoGenerateModalProps> = ({
  isOpen,
  onClose,
  onSuccess,
}) => {
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [selectedSubjectId, setSelectedSubjectId] = useState('');
  const [name, setName] = useState('');
  const [durationMinutes, setDurationMinutes] = useState(25);
  const [passingPercentage, setPassingPercentage] = useState(50);
  const [easyCount, setEasyCount] = useState(2);
  const [mediumCount, setMediumCount] = useState(2);
  const [hardCount, setHardCount] = useState(1);
  const [topicFilter, setTopicFilter] = useState('');

  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);

  const subjectSelectId = useId();
  const nameInputId = useId();
  const durationInputId = useId();
  const passingInputId = useId();
  const topicInputId = useId();
  const easyInputId = useId();
  const mediumInputId = useId();
  const hardInputId = useId();

  const { showToast } = useToast();

  useEffect(() => {
    if (!isOpen) return;

    const loadSubjects = async () => {
      try {
        setLoading(true);
        const res = await SubjectService.listSubjects();
        setSubjects(res.items || []);
        if (res.items?.length > 0 && !selectedSubjectId) {
          setSelectedSubjectId(res.items[0].id);
          setName(`Rapid Quiz - ${res.items[0].code}`);
        }
      } catch (err: unknown) {
        showToast(err instanceof Error ? err.message : 'Failed to load subjects', 'error');
      } finally {
        setLoading(false);
      }
    };

    loadSubjects();
  }, [isOpen]);

  if (!isOpen) return null;

  const handleSubjectChange = (id: string) => {
    setSelectedSubjectId(id);
    const sub = subjects.find((s) => s.id === id);
    if (sub) {
      setName(`Automated Assessment - ${sub.code}`);
    }
  };

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();

    const totalQuestions = easyCount + mediumCount + hardCount;
    if (totalQuestions <= 0) {
      showToast('Please specify at least 1 question across difficulty levels', 'error');
      return;
    }

    const now = new Date();
    const nextWeek = new Date();
    nextWeek.setDate(now.getDate() + 7);

    try {
      setGenerating(true);
      await examService.autoGenerateExam({
        subject_id: selectedSubjectId,
        name: name.trim() || 'Auto-Generated Examination',
        duration_minutes: Number(durationMinutes),
        passing_percentage: Number(passingPercentage),
        start_date: now.toISOString(),
        end_date: nextWeek.toISOString(),
        easy_count: Number(easyCount),
        medium_count: Number(mediumCount),
        hard_count: Number(hardCount),
        topic_filter: topicFilter.trim() || undefined,
        instructions: 'Auto-generated examination from the subject question bank. Answer all questions within the allocated time.',
      });

      showToast(`Successfully created examination with ${totalQuestions} sampled questions!`, 'success');
      onSuccess();
      onClose();
    } catch (err: unknown) {
      showToast(err instanceof Error ? err.message : 'Question generation failed', 'error');
    } finally {
      setGenerating(false);
    }
  };

  const totalQuestions = Number(easyCount) + Number(mediumCount) + Number(hardCount);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-xs">
      <div className="relative w-full max-w-lg bg-white dark:bg-zinc-900 rounded-2xl shadow-xl border border-zinc-200 dark:border-zinc-800 flex flex-col overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-zinc-200 dark:border-zinc-800 bg-gradient-to-r from-purple-500/10 to-indigo-500/10">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-purple-100 dark:bg-purple-900/40 text-purple-600 dark:text-purple-400">
              <Wand2 className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-zinc-900 dark:text-zinc-50">
                Auto-Generate Examination
              </h2>
              <p className="text-xs text-zinc-500 dark:text-zinc-400">
                Algorithmically assemble an exam from the question bank.
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Body */}
        {loading ? (
          <div className="py-16 flex justify-center">
            <LoadingSpinner size="md" />
          </div>
        ) : (
          <form onSubmit={handleGenerate} className="p-6 space-y-4">
            <div>
              <label htmlFor={subjectSelectId} className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                Target Subject *
              </label>
              <select
                id={subjectSelectId}
                value={selectedSubjectId}
                onChange={(e) => handleSubjectChange(e.target.value)}
                className="w-full px-3 py-2 text-sm rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-purple-500"
              >
                {subjects.map((sub) => (
                  <option key={sub.id} value={sub.id}>
                    {sub.code} - {sub.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor={nameInputId} className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                Exam Title *
              </label>
              <input
                id={nameInputId}
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full px-3 py-2 text-sm rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label htmlFor={durationInputId} className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                  Duration (Minutes)
                </label>
                <input
                  id={durationInputId}
                  type="number"
                  min="5"
                  max="180"
                  value={durationMinutes}
                  onChange={(e) => setDurationMinutes(Number(e.target.value))}
                  className="w-full px-3 py-2 text-sm rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
              <div>
                <label htmlFor={passingInputId} className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                  Pass Mark (%)
                </label>
                <input
                  id={passingInputId}
                  type="number"
                  min="1"
                  max="100"
                  value={passingPercentage}
                  onChange={(e) => setPassingPercentage(Number(e.target.value))}
                  className="w-full px-3 py-2 text-sm rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
            </div>

            {/* Difficulty Question Distribution */}
            <div className="p-3.5 rounded-xl border border-zinc-200 dark:border-zinc-800 bg-zinc-50/60 dark:bg-zinc-900/60 space-y-3">
              <div className="flex items-center justify-between text-xs font-bold text-zinc-900 dark:text-zinc-100">
                <span className="flex items-center gap-1.5">
                  <Sliders className="w-3.5 h-3.5 text-purple-600" />
                  Difficulty Breakdown
                </span>
                <span className="px-2 py-0.5 rounded bg-purple-100 dark:bg-purple-900/40 text-purple-700 dark:text-purple-300 font-semibold">
                  Total: {totalQuestions} Questions
                </span>
              </div>

              <div className="grid grid-cols-3 gap-2 text-xs">
                <div>
                  <label htmlFor={easyInputId} className="block text-zinc-600 dark:text-zinc-400 mb-1 font-medium">
                    Easy
                  </label>
                  <input
                    id={easyInputId}
                    type="number"
                    min="0"
                    max="50"
                    value={easyCount}
                    onChange={(e) => setEasyCount(Number(e.target.value))}
                    className="w-full px-2.5 py-1.5 rounded-md bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700"
                  />
                </div>
                <div>
                  <label htmlFor={mediumInputId} className="block text-zinc-600 dark:text-zinc-400 mb-1 font-medium">
                    Medium
                  </label>
                  <input
                    id={mediumInputId}
                    type="number"
                    min="0"
                    max="50"
                    value={mediumCount}
                    onChange={(e) => setMediumCount(Number(e.target.value))}
                    className="w-full px-2.5 py-1.5 rounded-md bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700"
                  />
                </div>
                <div>
                  <label htmlFor={hardInputId} className="block text-zinc-600 dark:text-zinc-400 mb-1 font-medium">
                    Hard
                  </label>
                  <input
                    id={hardInputId}
                    type="number"
                    min="0"
                    max="50"
                    value={hardCount}
                    onChange={(e) => setHardCount(Number(e.target.value))}
                    className="w-full px-2.5 py-1.5 rounded-md bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700"
                  />
                </div>
              </div>
            </div>

            <div>
              <label htmlFor={topicInputId} className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                Specific Topic Filter (Optional)
              </label>
              <input
                id={topicInputId}
                type="text"
                placeholder="e.g. Data Structures, Arrays, Mechanics"
                value={topicFilter}
                onChange={(e) => setTopicFilter(e.target.value)}
                className="w-full px-3 py-2 text-sm rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
            </div>

            <div className="pt-2 flex items-center justify-end gap-2 border-t border-zinc-200 dark:border-zinc-800">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 text-xs font-medium rounded-lg text-zinc-700 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={generating}
                className="px-4 py-2 text-xs font-semibold rounded-lg bg-purple-600 text-white hover:bg-purple-700 shadow-sm transition-colors flex items-center gap-1.5"
              >
                {generating ? <LoadingSpinner size="sm" /> : <Sparkles className="w-3.5 h-3.5" />}
                Generate & Save
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};
