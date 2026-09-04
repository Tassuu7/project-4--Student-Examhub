import React, { useState, useEffect, useCallback } from 'react';
import { Question, QuestionDifficulty } from '@/src/types/question.ts';
import { Subject } from '@/src/types/subject.ts';
import { QuestionService } from '@/src/services/questionService.ts';
import { SubjectService } from '@/src/services/subjectService.ts';
import { useToast } from '@/src/contexts/ToastContext.tsx';
import { QuestionFormModal } from './QuestionFormModal.tsx';
import { QuestionBulkImportModal } from './QuestionBulkImportModal.tsx';
import { SubjectListModal } from '@/src/components/subjects/SubjectListModal.tsx';
import { LoadingSpinner } from '@/src/components/common/LoadingSpinner.tsx';
import {
  Plus,
  Upload,
  Download,
  BookOpen,
  Search,
  Filter,
  Edit2,
  Trash2,
  HelpCircle,
  Layers,
  ChevronLeft,
  ChevronRight,
} from 'lucide-react';

interface QuestionListProps {
  userRole: 'admin' | 'teacher' | 'student';
}

export const QuestionList: React.FC<QuestionListProps> = ({ userRole }) => {
  const { showSuccess, showError } = useToast();
  const [questions, setQuestions] = useState<Question[]>([]);
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [loading, setLoading] = useState(true);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const pageSize = 10;

  // Filter states
  const [selectedSubject, setSelectedSubject] = useState<string>('');
  const [selectedDifficulty, setSelectedDifficulty] = useState<QuestionDifficulty | ''>('');
  const [searchQuery, setSearchQuery] = useState('');

  // Modals
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingQuestion, setEditingQuestion] = useState<Question | null>(null);
  const [isImportOpen, setIsImportOpen] = useState(false);
  const [isSubjectModalOpen, setIsSubjectModalOpen] = useState(false);

  const loadQuestions = useCallback(async () => {
    setLoading(true);
    try {
      const res = await QuestionService.listQuestions({
        subject_id: selectedSubject || undefined,
        difficulty: selectedDifficulty ? (selectedDifficulty as QuestionDifficulty) : undefined,
        search: searchQuery || undefined,
        page,
        page_size: pageSize,
      });
      setQuestions(res.items);
      setTotal(res.total);
    } catch {
      showError('Failed to load questions from question bank.');
    } finally {
      setLoading(false);
    }
  }, [selectedSubject, selectedDifficulty, searchQuery, page, pageSize, showError]);

  useEffect(() => {
    const fetchSubjects = async () => {
      try {
        const res = await SubjectService.listSubjects();
        setSubjects(res.items);
      } catch {
        // Ignored
      }
    };
    fetchSubjects();
  }, []);

  useEffect(() => {
    loadQuestions();
  }, [loadQuestions]);

  const handleDelete = async (questionId: string) => {
    if (!window.confirm('Are you sure you want to delete this question?')) {
      return;
    }
    try {
      await QuestionService.deleteQuestion(questionId);
      showSuccess('Question removed from the question bank.');
      loadQuestions();
    } catch (err: unknown) {
      showError(err instanceof Error ? err.message : 'Failed to delete question.');
    }
  };

  const handleExport = async () => {
    try {
      const blob = await QuestionService.exportCsv(selectedSubject || undefined);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `examhub_questions_${new Date().toISOString().split('T')[0]}.csv`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
      showSuccess('Questions exported successfully.');
    } catch {
      showError('Failed to export questions.');
    }
  };

  const totalPages = Math.ceil(total / pageSize) || 1;

  const getDifficultyBadge = (diff: QuestionDifficulty) => {
    switch (diff) {
      case 'Easy':
        return 'bg-emerald-50 text-emerald-700 border-emerald-200';
      case 'Medium':
        return 'bg-amber-50 text-amber-700 border-amber-200';
      case 'Hard':
        return 'bg-rose-50 text-rose-700 border-rose-200';
      default:
        return 'bg-stone-100 text-stone-700 border-stone-200';
    }
  };

  return (
    <div id="question-bank-container" className="space-y-6">
      {/* Top action header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-stone-900 tracking-tight">Question Bank</h2>
          <p className="text-xs text-stone-700 mt-0.5">
            Curate, tag, and organize multiple-choice evaluation questions
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <button
            id="manage-subjects-btn"
            onClick={() => setIsSubjectModalOpen(true)}
            className="flex items-center gap-1.5 px-3 py-2 text-xs font-medium text-stone-700 bg-white hover:bg-stone-50 border border-stone-300 rounded-lg shadow-2xs transition-colors"
          >
            <BookOpen className="w-3.5 h-3.5 text-stone-500" />
            <span>Subjects</span>
          </button>
          <button
            id="export-questions-btn"
            onClick={handleExport}
            className="flex items-center gap-1.5 px-3 py-2 text-xs font-medium text-stone-700 bg-white hover:bg-stone-50 border border-stone-300 rounded-lg shadow-2xs transition-colors"
          >
            <Download className="w-3.5 h-3.5 text-stone-500" />
            <span>Export CSV</span>
          </button>
          {userRole !== 'student' && (
            <>
              <button
                id="bulk-import-questions-btn"
                onClick={() => setIsImportOpen(true)}
                className="flex items-center gap-1.5 px-3 py-2 text-xs font-medium text-stone-700 bg-white hover:bg-stone-50 border border-stone-300 rounded-lg shadow-2xs transition-colors"
              >
                <Upload className="w-3.5 h-3.5 text-stone-500" />
                <span>Bulk Import</span>
              </button>
              <button
                id="create-question-btn"
                onClick={() => {
                  setEditingQuestion(null);
                  setIsFormOpen(true);
                }}
                className="flex items-center gap-1.5 px-3.5 py-2 text-xs font-medium text-white bg-amber-600 hover:bg-amber-700 rounded-lg shadow-2xs transition-colors"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>Add Question</span>
              </button>
            </>
          )}
        </div>
      </div>

      {/* Filter toolbar */}
      <div className="bg-white p-4 rounded-xl border border-stone-200 shadow-2xs flex flex-wrap items-center gap-3">
        <div className="relative flex-1 min-w-[200px]">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-stone-400" />
          <input
            id="question-search-input"
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search questions by keyword or topic..."
            className="w-full pl-9 pr-3 py-2 text-xs bg-stone-50 border border-stone-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:bg-white"
          />
        </div>

        <div className="flex items-center gap-2">
          <Filter className="w-3.5 h-3.5 text-stone-400 shrink-0" />
          <select
            id="filter-subject-select"
            value={selectedSubject}
            onChange={(e) => {
              setSelectedSubject(e.target.value);
              setPage(1);
            }}
            className="px-3 py-2 text-xs bg-stone-50 border border-stone-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:bg-white"
          >
            <option value="">All Subjects</option>
            {subjects.map((s) => (
              <option key={s.id} value={s.id}>
                {s.code} - {s.name}
              </option>
            ))}
          </select>

          <select
            id="filter-difficulty-select"
            value={selectedDifficulty}
            onChange={(e) => {
              setSelectedDifficulty(e.target.value as QuestionDifficulty | '');
              setPage(1);
            }}
            className="px-3 py-2 text-xs bg-stone-50 border border-stone-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:bg-white"
          >
            <option value="">All Difficulties</option>
            <option value="Easy">Easy</option>
            <option value="Medium">Medium</option>
            <option value="Hard">Hard</option>
          </select>
        </div>
      </div>

      {/* Questions list table */}
      <div className="bg-white rounded-xl border border-stone-200 shadow-2xs overflow-hidden">
        {loading ? (
          <LoadingSpinner size="lg" label="Retrieving question catalog..." className="py-16" />
        ) : questions.length === 0 ? (
          <div className="text-center py-16 px-4">
            <HelpCircle className="w-10 h-10 text-stone-300 mx-auto mb-2" />
            <p className="text-sm font-semibold text-stone-700">No questions found</p>
            <p className="text-xs text-stone-700 mt-1 max-w-sm mx-auto">
              Try adjusting your search query or subject filters, or click &quot;Add Question&quot; to author your first question.
            </p>
          </div>
        ) : (
          <div className="divide-y divide-stone-200">
            {questions.map((q, idx) => (
              <div
                key={q.id}
                id={`question-row-${q.id}`}
                className="p-5 hover:bg-stone-50/60 transition-colors flex flex-col md:flex-row items-start md:items-center justify-between gap-4"
              >
                <div className="flex-1 space-y-2">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="font-mono text-xs font-bold px-2 py-0.5 rounded bg-stone-100 text-stone-800 border border-stone-200">
                      {q.subject_code}
                    </span>
                    <span
                      className={`text-[11px] font-semibold px-2 py-0.5 rounded-full border ${getDifficultyBadge(
                        q.difficulty
                      )}`}
                    >
                      {q.difficulty}
                    </span>
                    <span className="text-xs text-stone-700 font-medium">
                      Marks: <strong className="text-stone-800">{q.marks}</strong>
                    </span>
                    {q.topic && (
                      <span className="text-[11px] text-stone-700 bg-stone-100 px-2 py-0.5 rounded-md">
                        {q.topic}
                      </span>
                    )}
                  </div>

                  <p className="text-sm font-semibold text-stone-900 leading-snug">{q.question_text}</p>

                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2 pt-1 text-xs">
                    {(['A', 'B', 'C', 'D'] as const).map((opt) => {
                      const text = q[`option_${opt.toLowerCase()}` as keyof Question];
                      const isCorrect = q.correct_answer === opt;
                      return (
                        <div
                          key={opt}
                          className={`px-2.5 py-1 rounded border ${
                            isCorrect
                              ? 'bg-amber-50 border-amber-300 font-medium text-amber-900'
                              : 'bg-white border-stone-200 text-stone-600'
                          }`}
                        >
                          <span className="font-bold mr-1">{opt}:</span>
                          <span className="truncate">{text as string}</span>
                        </div>
                      );
                    })}
                  </div>

                  {q.explanation && (
                    <p className="text-[11px] text-stone-700 italic pt-1">
                      <span className="font-medium not-italic text-stone-700">Explanation:</span> {q.explanation}
                    </p>
                  )}
                </div>

                {userRole !== 'student' && (
                  <div className="flex items-center gap-2 shrink-0 self-end md:self-center">
                    <button
                      id={`edit-question-${q.id}`}
                      onClick={() => {
                        setEditingQuestion(q);
                        setIsFormOpen(true);
                      }}
                      className="p-1.5 text-stone-500 hover:text-amber-700 hover:bg-stone-100 rounded-lg transition-colors"
                      title="Edit Question"
                    >
                      <Edit2 className="w-4 h-4" />
                    </button>
                    <button
                      id={`delete-question-${q.id}`}
                      onClick={() => handleDelete(q.id)}
                      className="p-1.5 text-stone-500 hover:text-rose-600 hover:bg-stone-100 rounded-lg transition-colors"
                      title="Delete Question"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {/* Pagination bar */}
        {!loading && questions.length > 0 && (
          <div className="px-6 py-3.5 bg-stone-50 border-t border-stone-200 flex items-center justify-between text-xs text-stone-500">
            <span>
              Showing {(page - 1) * pageSize + 1} to {Math.min(page * pageSize, total)} of {total} questions
            </span>
            <div className="flex items-center gap-2">
              <button
                id="pagination-prev-btn"
                disabled={page <= 1}
                onClick={() => setPage((p) => p - 1)}
                className="p-1.5 rounded border border-stone-300 hover:bg-white disabled:opacity-40 transition-colors"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <span className="font-medium text-stone-700">
                Page {page} of {totalPages}
              </span>
              <button
                id="pagination-next-btn"
                disabled={page >= totalPages}
                onClick={() => setPage((p) => p + 1)}
                className="p-1.5 rounded border border-stone-300 hover:bg-white disabled:opacity-40 transition-colors"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Modal Dialogs */}
      <QuestionFormModal
        isOpen={isFormOpen}
        onClose={() => {
          setIsFormOpen(false);
          setEditingQuestion(null);
        }}
        onSaved={loadQuestions}
        editingQuestion={editingQuestion}
      />

      <QuestionBulkImportModal
        isOpen={isImportOpen}
        onClose={() => setIsImportOpen(false)}
        onImportSuccess={loadQuestions}
      />

      <SubjectListModal
        isOpen={isSubjectModalOpen}
        onClose={() => setIsSubjectModalOpen(false)}
        isAdmin={userRole === 'admin'}
      />
    </div>
  );
};
