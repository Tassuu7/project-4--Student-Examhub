/**
 * ExamHub - Create/Edit Examination Modal with Question and Student Assignment
 */

import React, { useState, useEffect, useId } from 'react';
import {
  X,
  Plus,
  CheckSquare,
  Square,
  Clock,
  Award,
  Users,
  BookOpen,
  Filter,
  AlertCircle
} from 'lucide-react';
import { Subject } from '../../types/subject';
import { Question } from '../../types/question';
import { Exam } from '../../types/exam';
import { StudentListItem, examService } from '../../services/examService';
import { SubjectService } from '../../services/subjectService';
import { QuestionService } from '../../services/questionService';
import { useToast } from '../../contexts/ToastContext';
import { LoadingSpinner } from '../common/LoadingSpinner';

interface ExamFormModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  examToEdit?: Exam | null;
}

export const ExamFormModal: React.FC<ExamFormModalProps> = ({
  isOpen,
  onClose,
  onSuccess,
  examToEdit,
}) => {
  const [activeTab, setActiveTab] = useState<'details' | 'questions' | 'students'>('details');

  // Form State
  const [name, setName] = useState('');
  const [subjectId, setSubjectId] = useState('');
  const [description, setDescription] = useState('');
  const [durationMinutes, setDurationMinutes] = useState(30);
  const [passingPercentage, setPassingPercentage] = useState(50);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [instructions, setInstructions] = useState('1. Answer all questions.\n2. Do not switch browser tabs.\n3. Exam will auto-submit when the timer expires.');
  const [requireCameraProctoring, setRequireCameraProctoring] = useState(true);

  // Pickers State
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [availableQuestions, setAvailableQuestions] = useState<Question[]>([]);
  const [selectedQuestionIds, setSelectedQuestionIds] = useState<string[]>([]);
  const [availableStudents, setAvailableStudents] = useState<StudentListItem[]>([]);
  const [selectedStudentIds, setSelectedStudentIds] = useState<string[]>([]);

  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [questionFilter, setQuestionFilter] = useState('');

  const nameInputId = useId();
  const subjectInputId = useId();
  const durationInputId = useId();
  const passingInputId = useId();
  const startDateInputId = useId();
  const endDateInputId = useId();
  const descriptionInputId = useId();
  const instructionsInputId = useId();

  const { showToast } = useToast();

  useEffect(() => {
    if (!isOpen) return;

    const now = new Date();
    const nextWeek = new Date();
    nextWeek.setDate(now.getDate() + 7);

    if (examToEdit) {
      setName(examToEdit.name || '');
      setSubjectId(examToEdit.subject_id || '');
      setDescription(examToEdit.description || '');
      setDurationMinutes(examToEdit.duration_minutes || 30);
      setPassingPercentage(examToEdit.passing_percentage || 50);
      setStartDate(
        examToEdit.start_date
          ? new Date(examToEdit.start_date).toISOString().slice(0, 16)
          : now.toISOString().slice(0, 16)
      );
      setEndDate(
        examToEdit.end_date
          ? new Date(examToEdit.end_date).toISOString().slice(0, 16)
          : nextWeek.toISOString().slice(0, 16)
      );
      setInstructions(
        examToEdit.instructions ||
          '1. Answer all questions.\n2. Do not switch browser tabs.\n3. Exam will auto-submit when the timer expires.'
      );
      setRequireCameraProctoring(examToEdit.require_camera_proctoring ?? true);
    } else {
      setName('');
      setDescription('');
      setDurationMinutes(30);
      setPassingPercentage(50);
      setStartDate(now.toISOString().slice(0, 16));
      setEndDate(nextWeek.toISOString().slice(0, 16));
      setInstructions(
        '1. Answer all questions.\n2. Do not switch browser tabs.\n3. Exam will auto-submit when the timer expires.'
      );
      setRequireCameraProctoring(true);
      setSelectedQuestionIds([]);
      setSelectedStudentIds([]);
    }

    const loadMetadata = async () => {
      try {
        setLoading(true);
        const [subs, stus, details] = await Promise.all([
          SubjectService.listSubjects(),
          examService.listAvailableStudents(),
          examToEdit ? examService.getExamDetails(examToEdit.id).catch(() => null) : Promise.resolve(null),
        ]);
        setSubjects(subs.items || []);
        setAvailableStudents(stus.items || []);

        if (examToEdit && details) {
          if (details.questions && Array.isArray(details.questions)) {
            setSelectedQuestionIds(details.questions.map((q: any) => q.question_id));
          }
          if (details.assigned_students && Array.isArray(details.assigned_students)) {
            setSelectedStudentIds(details.assigned_students.map((s: any) => s.student_id));
          }
        } else if (subs.items?.length > 0 && !subjectId) {
          setSubjectId(subs.items[0].id);
        }
      } catch (err: unknown) {
        showToast(err instanceof Error ? err.message : 'Failed to load options', 'error');
      } finally {
        setLoading(false);
      }
    };

    loadMetadata();
  }, [isOpen, examToEdit]);

  // Load questions when subject changes
  useEffect(() => {
    if (!subjectId || !isOpen) return;
    const loadQuestions = async () => {
      try {
        const res = await QuestionService.listQuestions({ subject_id: subjectId, page_size: 100 });
        setAvailableQuestions(res.items || []);
      } catch {
        setAvailableQuestions([]);
      }
    };
    loadQuestions();
  }, [subjectId, isOpen]);

  if (!isOpen) return null;

  const toggleQuestion = (id: string) => {
    setSelectedQuestionIds((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    );
  };

  const selectAllQuestions = () => {
    if (selectedQuestionIds.length === availableQuestions.length) {
      setSelectedQuestionIds([]);
    } else {
      setSelectedQuestionIds(availableQuestions.map((q) => q.id));
    }
  };

  const toggleStudent = (id: string) => {
    setSelectedStudentIds((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    );
  };

  const selectAllStudents = () => {
    if (selectedStudentIds.length === availableStudents.length) {
      setSelectedStudentIds([]);
    } else {
      setSelectedStudentIds(availableStudents.map((s) => s.student_id));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!name.trim()) {
      showToast('Exam name is required', 'error');
      setActiveTab('details');
      return;
    }
    if (!subjectId) {
      showToast('Please select a subject', 'error');
      setActiveTab('details');
      return;
    }
    if (selectedQuestionIds.length === 0) {
      showToast('Please select at least one question for the exam', 'error');
      setActiveTab('questions');
      return;
    }

    try {
      setSubmitting(true);
      const payload = {
        name: name.trim(),
        subject_id: subjectId,
        description: description.trim() || undefined,
        duration_minutes: Number(durationMinutes),
        passing_percentage: Number(passingPercentage),
        start_date: new Date(startDate).toISOString(),
        end_date: new Date(endDate).toISOString(),
        instructions: instructions.trim() || undefined,
        require_camera_proctoring: requireCameraProctoring,
        question_ids: selectedQuestionIds,
        student_ids: selectedStudentIds,
      };

      if (examToEdit) {
        await examService.updateExam(examToEdit.id, payload);
        showToast('Examination updated successfully!', 'success');
      } else {
        await examService.createExam(payload);
        showToast('Examination created successfully!', 'success');
      }

      onSuccess();
      onClose();
    } catch (err: unknown) {
      showToast(err instanceof Error ? err.message : 'Failed to save examination', 'error');
    } finally {
      setSubmitting(false);
    }
  };

  const filteredQuestions = availableQuestions.filter((q) =>
    q.question_text.toLowerCase().includes(questionFilter.toLowerCase()) ||
    q.difficulty.toLowerCase().includes(questionFilter.toLowerCase()) ||
    (q.topic && q.topic.toLowerCase().includes(questionFilter.toLowerCase()))
  );

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-xs overflow-y-auto">
      <div className="relative w-full max-w-3xl bg-white dark:bg-zinc-900 rounded-2xl shadow-xl border border-zinc-200 dark:border-zinc-800 flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-zinc-200 dark:border-zinc-800">
          <div>
            <h2 className="text-lg font-bold text-zinc-900 dark:text-zinc-50">
              {examToEdit ? `Edit Examination: ${examToEdit.name}` : 'Create New Examination'}
            </h2>
            <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">
              {examToEdit
                ? 'Update exam settings, questions, and assigned students.'
                : 'Set details, assign questions from the bank, and enroll students.'}
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab Navigation */}
        <div className="flex border-b border-zinc-200 dark:border-zinc-800 px-6 bg-zinc-50/50 dark:bg-zinc-900/50">
          <button
            type="button"
            onClick={() => setActiveTab('details')}
            className={`py-3 px-4 text-xs font-semibold border-b-2 transition-colors ${
              activeTab === 'details'
                ? 'border-indigo-600 text-indigo-600 dark:text-indigo-400'
                : 'border-transparent text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300'
            }`}
          >
            1. Exam Configuration
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('questions')}
            className={`py-3 px-4 text-xs font-semibold border-b-2 transition-colors flex items-center gap-1.5 ${
              activeTab === 'questions'
                ? 'border-indigo-600 text-indigo-600 dark:text-indigo-400'
                : 'border-transparent text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300'
            }`}
          >
            2. Question Selection ({selectedQuestionIds.length})
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('students')}
            className={`py-3 px-4 text-xs font-semibold border-b-2 transition-colors flex items-center gap-1.5 ${
              activeTab === 'students'
                ? 'border-indigo-600 text-indigo-600 dark:text-indigo-400'
                : 'border-transparent text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300'
            }`}
          >
            3. Student Enrollment ({selectedStudentIds.length})
          </button>
        </div>

        {/* Body Content */}
        <div className="p-6 overflow-y-auto flex-1">
          {loading ? (
            <div className="py-16 flex justify-center">
              <LoadingSpinner size="md" />
            </div>
          ) : (
            <form id="exam-create-form" onSubmit={handleSubmit}>
              {/* Tab 1: Details */}
              {activeTab === 'details' && (
                <div className="space-y-4">
                  <div>
                    <label htmlFor={nameInputId} className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                      Exam Title *
                    </label>
                    <input
                      id={nameInputId}
                      type="text"
                      required
                      placeholder="e.g. Mid-Term Examination 2026"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      className="w-full px-3 py-2 text-sm rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label htmlFor={subjectInputId} className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                        Subject Course *
                      </label>
                      <select
                        id={subjectInputId}
                        value={subjectId}
                        onChange={(e) => setSubjectId(e.target.value)}
                        className="w-full px-3 py-2 text-sm rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      >
                        {subjects.map((s) => (
                          <option key={s.id} value={s.id}>
                            {s.code} - {s.name}
                          </option>
                        ))}
                      </select>
                    </div>

                    <div>
                      <label htmlFor={durationInputId} className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                        Duration (Minutes) *
                      </label>
                      <input
                        id={durationInputId}
                        type="number"
                        min="5"
                        max="300"
                        required
                        value={durationMinutes}
                        onChange={(e) => setDurationMinutes(Number(e.target.value))}
                        className="w-full px-3 py-2 text-sm rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label htmlFor={passingInputId} className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                        Passing Percentage (%) *
                      </label>
                      <input
                        id={passingInputId}
                        type="number"
                        min="1"
                        max="100"
                        required
                        value={passingPercentage}
                        onChange={(e) => setPassingPercentage(Number(e.target.value))}
                        className="w-full px-3 py-2 text-sm rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      />
                    </div>

                    <div>
                      <label htmlFor={descriptionInputId} className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                        Brief Description
                      </label>
                      <input
                        id={descriptionInputId}
                        type="text"
                        placeholder="Semester unit assessment"
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        className="w-full px-3 py-2 text-sm rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label htmlFor={startDateInputId} className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                        Start Date & Time *
                      </label>
                      <input
                        id={startDateInputId}
                        type="datetime-local"
                        required
                        value={startDate}
                        onChange={(e) => setStartDate(e.target.value)}
                        className="w-full px-3 py-2 text-sm rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      />
                    </div>

                    <div>
                      <label htmlFor={endDateInputId} className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                        End Date & Time *
                      </label>
                      <input
                        id={endDateInputId}
                        type="datetime-local"
                        required
                        value={endDate}
                        onChange={(e) => setEndDate(e.target.value)}
                        className="w-full px-3 py-2 text-sm rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      />
                    </div>
                  </div>

                  <div>
                    <label htmlFor={instructionsInputId} className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                      Student Instructions
                    </label>
                    <textarea
                      id={instructionsInputId}
                      rows={3}
                      value={instructions}
                      onChange={(e) => setInstructions(e.target.value)}
                      className="w-full px-3 py-2 text-sm rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>

                  {/* Camera & Continuous Proctoring Setting */}
                  <div className="p-4 rounded-xl border border-indigo-200 dark:border-indigo-900/50 bg-indigo-50/50 dark:bg-indigo-950/20 flex items-start gap-3">
                    <input
                      id="toggle-camera-proctoring"
                      type="checkbox"
                      checked={requireCameraProctoring}
                      onChange={(e) => setRequireCameraProctoring(e.target.checked)}
                      className="mt-1 h-4 w-4 text-indigo-600 rounded border-zinc-300 dark:border-zinc-700 focus:ring-indigo-500 cursor-pointer"
                    />
                    <label htmlFor="toggle-camera-proctoring" className="cursor-pointer">
                      <span className="block text-xs font-bold text-zinc-900 dark:text-zinc-100">
                        Require Live Camera Access & Continuous Proctoring
                      </span>
                      <span className="block text-[11px] text-zinc-500 dark:text-zinc-400 mt-0.5 leading-normal">
                        When approved by the teacher, candidate will be prompted for live webcam permissions. The system monitors face presence, gaze direction, tab switching, and window focus during the entire assessment.
                      </span>
                    </label>
                  </div>
                </div>
              )}

              {/* Tab 2: Question Selection */}
              {activeTab === 'questions' && (
                <div className="space-y-4">
                  <div className="flex items-center justify-between gap-3">
                    <div className="relative flex-1">
                      <input
                        type="text"
                        placeholder="Search questions by text or topic..."
                        value={questionFilter}
                        onChange={(e) => setQuestionFilter(e.target.value)}
                        className="w-full pl-3 pr-4 py-1.5 text-xs rounded-lg bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700"
                      />
                    </div>
                    <button
                      type="button"
                      onClick={selectAllQuestions}
                      className="text-xs font-semibold text-indigo-600 dark:text-indigo-400 hover:underline whitespace-nowrap"
                    >
                      {selectedQuestionIds.length === availableQuestions.length
                        ? 'Deselect All'
                        : 'Select All Questions'}
                    </button>
                  </div>

                  {availableQuestions.length === 0 ? (
                    <div className="text-center py-10 text-xs text-zinc-500">
                      No questions found for this subject in the Question Bank.
                    </div>
                  ) : (
                    <div className="space-y-2 max-h-[340px] overflow-y-auto pr-1">
                      {filteredQuestions.map((q) => {
                        const isSelected = selectedQuestionIds.includes(q.id);
                        return (
                          <div
                            key={q.id}
                            onClick={() => toggleQuestion(q.id)}
                            className={`p-3 rounded-lg border text-xs cursor-pointer transition-all flex items-start gap-3 ${
                              isSelected
                                ? 'border-indigo-500 bg-indigo-50/50 dark:bg-indigo-950/20'
                                : 'border-zinc-200 dark:border-zinc-800 hover:border-zinc-300'
                            }`}
                          >
                            <div className="mt-0.5">
                              {isSelected ? (
                                <CheckSquare className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
                              ) : (
                                <Square className="w-4 h-4 text-zinc-400" />
                              )}
                            </div>
                            <div className="flex-1 min-w-0">
                              <p className="font-medium text-zinc-900 dark:text-zinc-100">
                                {q.question_text}
                              </p>
                              <div className="flex items-center gap-2 mt-1.5 text-[11px] text-zinc-500">
                                <span className="px-1.5 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 font-medium">
                                  {q.difficulty}
                                </span>
                                {q.topic && <span>Topic: {q.topic}</span>}
                                <span>{q.marks || 1} mark(s)</span>
                              </div>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>
              )}

              {/* Tab 3: Student Enrollment */}
              {activeTab === 'students' && (
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <p className="text-xs text-zinc-500">
                      Select which enrolled students are granted access to attempt this examination.
                    </p>
                    <button
                      type="button"
                      onClick={selectAllStudents}
                      className="text-xs font-semibold text-indigo-600 dark:text-indigo-400 hover:underline"
                    >
                      {selectedStudentIds.length === availableStudents.length
                        ? 'Deselect All'
                        : 'Select All Students'}
                    </button>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 max-h-[340px] overflow-y-auto pr-1">
                    {availableStudents.map((stu) => {
                      const isSelected = selectedStudentIds.includes(stu.student_id);
                      return (
                        <div
                          key={stu.student_id}
                          onClick={() => toggleStudent(stu.student_id)}
                          className={`p-3 rounded-lg border text-xs cursor-pointer transition-all flex items-center gap-3 ${
                            isSelected
                              ? 'border-indigo-500 bg-indigo-50/50 dark:bg-indigo-950/20'
                              : 'border-zinc-200 dark:border-zinc-800 hover:border-zinc-300'
                          }`}
                        >
                          {isSelected ? (
                            <CheckSquare className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
                          ) : (
                            <Square className="w-4 h-4 text-zinc-400" />
                          )}
                          <div className="min-w-0">
                            <p className="font-medium text-zinc-900 dark:text-zinc-100 truncate">
                              {stu.full_name}
                            </p>
                            <p className="text-[11px] text-zinc-500 truncate">
                              Roll: {stu.student_id_code} {stu.department ? `• ${stu.department}` : ''}
                            </p>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
            </form>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between px-6 py-4 border-t border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-900/50">
          <div className="text-xs text-zinc-500">
            {selectedQuestionIds.length} question(s) • {selectedStudentIds.length} student(s) selected
          </div>
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-xs font-medium rounded-lg text-zinc-700 dark:text-zinc-300 hover:bg-zinc-200 dark:hover:bg-zinc-800 transition-colors"
            >
              Cancel
            </button>
            {activeTab !== 'students' && (
              <button
                type="button"
                onClick={() =>
                  setActiveTab(activeTab === 'details' ? 'questions' : 'students')
                }
                className="px-4 py-2 text-xs font-semibold rounded-lg bg-zinc-900 text-white dark:bg-zinc-100 dark:text-zinc-900 hover:opacity-90 transition-opacity"
              >
                Next Step →
              </button>
            )}
            <button
              type="submit"
              form="exam-create-form"
              disabled={submitting}
              className="px-5 py-2 text-xs font-semibold rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 shadow-sm transition-colors flex items-center gap-1.5"
            >
              {submitting && <LoadingSpinner size="sm" />}
              {examToEdit ? 'Save Changes' : 'Publish Examination'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
