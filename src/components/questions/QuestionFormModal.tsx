import React, { useState, useEffect } from 'react';
import { Question, QuestionFormData, QuestionDifficulty, CorrectOption } from '@/src/types/question.ts';
import { Subject } from '@/src/types/subject.ts';
import { SubjectService } from '@/src/services/subjectService.ts';
import { QuestionService } from '@/src/services/questionService.ts';
import { useToast } from '@/src/contexts/ToastContext.tsx';
import { X, Check, HelpCircle } from 'lucide-react';
import { LoadingSpinner } from '@/src/components/common/LoadingSpinner.tsx';

interface QuestionFormModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSaved: () => void;
  editingQuestion?: Question | null;
}

export const QuestionFormModal: React.FC<QuestionFormModalProps> = ({
  isOpen,
  onClose,
  onSaved,
  editingQuestion,
}) => {
  const { showSuccess, showError } = useToast();
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [loadingSubjects, setLoadingSubjects] = useState(false);
  const [saving, setSaving] = useState(false);

  const [formData, setFormData] = useState<QuestionFormData>({
    subject_id: '',
    question_text: '',
    option_a: '',
    option_b: '',
    option_c: '',
    option_d: '',
    correct_answer: 'A',
    marks: 1.0,
    difficulty: 'Medium',
    topic: '',
    explanation: '',
  });

  useEffect(() => {
    if (isOpen) {
      loadSubjects();
      if (editingQuestion) {
        setFormData({
          subject_id: editingQuestion.subject_id,
          question_text: editingQuestion.question_text,
          option_a: editingQuestion.option_a,
          option_b: editingQuestion.option_b,
          option_c: editingQuestion.option_c,
          option_d: editingQuestion.option_d,
          correct_answer: editingQuestion.correct_answer,
          marks: editingQuestion.marks,
          difficulty: editingQuestion.difficulty,
          topic: editingQuestion.topic || '',
          explanation: editingQuestion.explanation || '',
        });
      } else {
        setFormData({
          subject_id: '',
          question_text: '',
          option_a: '',
          option_b: '',
          option_c: '',
          option_d: '',
          correct_answer: 'A',
          marks: 1.0,
          difficulty: 'Medium',
          topic: '',
          explanation: '',
        });
      }
    }
  }, [isOpen, editingQuestion]);

  const loadSubjects = async () => {
    setLoadingSubjects(true);
    try {
      const res = await SubjectService.listSubjects();
      setSubjects(res.items);
      if (!editingQuestion && res.items.length > 0) {
        setFormData((prev) => ({ ...prev, subject_id: res.items[0].id }));
      }
    } catch {
      showError('Failed to load academic subjects.');
    } finally {
      setLoadingSubjects(false);
    }
  };

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.subject_id) {
      showError('Please select a subject.');
      return;
    }
    if (!formData.question_text.trim()) {
      showError('Question text cannot be blank.');
      return;
    }
    if (!formData.option_a.trim() || !formData.option_b.trim() || !formData.option_c.trim() || !formData.option_d.trim()) {
      showError('All 4 multiple choice options (A, B, C, D) are required.');
      return;
    }

    setSaving(true);
    try {
      if (editingQuestion) {
        await QuestionService.updateQuestion(editingQuestion.id, formData);
        showSuccess('Question updated successfully.');
      } else {
        await QuestionService.createQuestion(formData);
        showSuccess('New question added to the Question Bank.');
      }
      onSaved();
      onClose();
    } catch (err: unknown) {
      showError(err instanceof Error ? err.message : 'Failed to save question.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div id="question-form-modal-overlay" className="fixed inset-0 z-50 bg-stone-900/50 backdrop-blur-xs flex items-center justify-center p-4 overflow-y-auto">
      <div id="question-form-modal-container" className="bg-white rounded-xl shadow-xl border border-stone-200 w-full max-w-2xl overflow-hidden my-8">
        <div className="flex items-center justify-between px-6 py-4 border-b border-stone-200 bg-stone-50">
          <div>
            <h3 className="text-base font-semibold text-stone-900">
              {editingQuestion ? 'Edit Question' : 'Add New Multiple Choice Question'}
            </h3>
            <p className="text-xs text-stone-500">Configure question stem, options, grading weight, and explanation</p>
          </div>
          <button
            id="close-question-modal-btn"
            onClick={onClose}
            className="text-stone-400 hover:text-stone-700 p-1 rounded-md transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-semibold text-stone-700 mb-1">Subject</label>
              {loadingSubjects ? (
                <div className="text-xs text-stone-500 py-2">Loading subjects...</div>
              ) : (
                <select
                  id="question-subject-select"
                  value={formData.subject_id}
                  onChange={(e) => setFormData({ ...formData, subject_id: e.target.value })}
                  className="w-full px-3 py-2 text-sm bg-stone-50 border border-stone-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:bg-white"
                  required
                >
                  {subjects.map((sub) => (
                    <option key={sub.id} value={sub.id}>
                      {sub.code} - {sub.name}
                    </option>
                  ))}
                </select>
              )}
            </div>

            <div>
              <label className="block text-xs font-semibold text-stone-700 mb-1">Difficulty</label>
              <select
                id="question-difficulty-select"
                value={formData.difficulty}
                onChange={(e) => setFormData({ ...formData, difficulty: e.target.value as QuestionDifficulty })}
                className="w-full px-3 py-2 text-sm bg-stone-50 border border-stone-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:bg-white"
              >
                <option value="Easy">Easy</option>
                <option value="Medium">Medium</option>
                <option value="Hard">Hard</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-stone-700 mb-1">Marks</label>
              <input
                id="question-marks-input"
                type="number"
                min="0.5"
                step="0.5"
                max="50"
                value={formData.marks}
                onChange={(e) => setFormData({ ...formData, marks: parseFloat(e.target.value) || 1 })}
                className="w-full px-3 py-2 text-sm bg-stone-50 border border-stone-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:bg-white"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-stone-700 mb-1">Question Statement</label>
            <textarea
              id="question-statement-input"
              rows={3}
              value={formData.question_text}
              onChange={(e) => setFormData({ ...formData, question_text: e.target.value })}
              placeholder="Enter the complete question stem or scenario..."
              className="w-full px-3 py-2 text-sm bg-stone-50 border border-stone-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:bg-white"
              required
            />
          </div>

          <div className="space-y-2.5">
            <label className="block text-xs font-semibold text-stone-700">
              Options (Select the radio button for the correct answer)
            </label>

            {(['A', 'B', 'C', 'D'] as const).map((optKey) => {
              const fieldKey = `option_${optKey.toLowerCase()}` as keyof QuestionFormData;
              const isCorrect = formData.correct_answer === optKey;

              return (
                <div
                  key={optKey}
                  className={`flex items-center gap-3 p-2.5 rounded-lg border transition-colors ${
                    isCorrect ? 'bg-amber-50/60 border-amber-300 ring-1 ring-amber-400' : 'bg-stone-50 border-stone-200'
                  }`}
                >
                  <label className="flex items-center gap-2 cursor-pointer font-bold text-xs text-stone-800">
                    <input
                      type="radio"
                      name="correct_answer"
                      value={optKey}
                      checked={isCorrect}
                      onChange={() => setFormData({ ...formData, correct_answer: optKey as CorrectOption })}
                      className="text-amber-600 focus:ring-amber-500"
                    />
                    <span>Option {optKey}</span>
                  </label>
                  <input
                    type="text"
                    id={`option-${optKey.toLowerCase()}-input`}
                    value={formData[fieldKey] as string}
                    onChange={(e) => setFormData({ ...formData, [fieldKey]: e.target.value })}
                    placeholder={`Answer choice for ${optKey}...`}
                    className="flex-1 px-3 py-1.5 text-sm bg-white border border-stone-300 rounded-md focus:outline-none focus:ring-1 focus:ring-amber-500"
                    required
                  />
                </div>
              );
            })}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
            <div>
              <label className="block text-xs font-semibold text-stone-700 mb-1">Topic / Category (Optional)</label>
              <input
                id="question-topic-input"
                type="text"
                value={formData.topic}
                onChange={(e) => setFormData({ ...formData, topic: e.target.value })}
                placeholder="e.g. Recursion, Normalization, Asymptotics"
                className="w-full px-3 py-2 text-sm bg-stone-50 border border-stone-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:bg-white"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-stone-700 mb-1">Explanation (Post-Exam Review)</label>
              <input
                id="question-explanation-input"
                type="text"
                value={formData.explanation}
                onChange={(e) => setFormData({ ...formData, explanation: e.target.value })}
                placeholder="Brief justification shown when review is enabled"
                className="w-full px-3 py-2 text-sm bg-stone-50 border border-stone-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:bg-white"
              />
            </div>
          </div>

          <div className="flex items-center justify-end gap-3 pt-4 border-t border-stone-200 mt-4">
            <button
              id="cancel-question-btn"
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-stone-700 hover:bg-stone-100 rounded-lg transition-colors"
            >
              Cancel
            </button>
            <button
              id="save-question-submit-btn"
              type="submit"
              disabled={saving}
              className="flex items-center gap-2 px-5 py-2 text-sm font-medium text-white bg-amber-600 hover:bg-amber-700 rounded-lg shadow-sm transition-colors disabled:opacity-50"
            >
              {saving ? <LoadingSpinner size="sm" /> : <Check className="w-4 h-4" />}
              <span>{editingQuestion ? 'Save Changes' : 'Create Question'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
