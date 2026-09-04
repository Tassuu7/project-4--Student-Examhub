/**
 * ExamHub - Teacher/Admin Exam Management Dashboard
 */

import React, { useState, useEffect, useId } from 'react';
import {
  Plus,
  Wand2,
  Calendar,
  Clock,
  Award,
  Users,
  Search,
  CheckCircle,
  PlayCircle,
  FileText,
  AlertCircle
} from 'lucide-react';
import { Exam, ExamStatus } from '../../types/exam';
import { Subject } from '../../types/subject';
import { examService } from '../../services/examService';
import { SubjectService } from '../../services/subjectService';
import { useToast } from '../../contexts/ToastContext';
import { LoadingSpinner } from '../common/LoadingSpinner';

interface ExamListProps {
  onCreateClick: () => void;
  onAutoGenerateClick: () => void;
  onViewResults: (exam: Exam) => void;
  onSelectExam?: (exam: Exam) => void;
}

export const ExamList: React.FC<ExamListProps> = ({
  onCreateClick,
  onAutoGenerateClick,
  onViewResults,
}) => {
  const [exams, setExams] = useState<Exam[]>([]);
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedSubject, setSelectedSubject] = useState<string>('');
  const [selectedStatus, setSelectedStatus] = useState<string>('');
  const [searchQuery, setSearchQuery] = useState('');
  const [actionLoading, setActionLoading] = useState<string | null>(null);

  const subjectFilterId = useId();
  const statusFilterId = useId();
  const searchInputId = useId();

  const { showToast } = useToast();

  const loadData = async () => {
    try {
      setLoading(true);
      const [examsRes, subjectsRes] = await Promise.all([
        examService.listExams({
          subject_id: selectedSubject || undefined,
          status: selectedStatus || undefined,
          search: searchQuery || undefined,
        }),
        SubjectService.listSubjects(),
      ]);
      setExams(examsRes.items || []);
      setSubjects(subjectsRes.items || []);
    } catch (err: unknown) {
      showToast(err instanceof Error ? err.message : 'Failed to load examinations', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [selectedSubject, selectedStatus]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    loadData();
  };

  const handleStatusChange = async (examId: string, newStatus: ExamStatus) => {
    try {
      setActionLoading(examId);
      await examService.updateExamStatus(examId, newStatus);
      showToast(`Exam marked as ${newStatus}`, 'success');
      setExams((prev) =>
        prev.map((e) => (e.id === examId ? { ...e, status: newStatus } : e))
      );
    } catch (err: unknown) {
      showToast(err instanceof Error ? err.message : 'Failed to update exam status', 'error');
    } finally {
      setActionLoading(null);
    }
  };

  const getStatusBadge = (status: ExamStatus) => {
    switch (status) {
      case 'active':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
            Active
          </span>
        );
      case 'scheduled':
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-300">
            Scheduled
          </span>
        );
      case 'completed':
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-zinc-100 text-zinc-800 dark:bg-zinc-800 dark:text-zinc-300">
            Completed
          </span>
        );
      case 'cancelled':
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-rose-100 text-rose-800 dark:bg-rose-900/40 dark:text-rose-300">
            Cancelled
          </span>
        );
      case 'draft':
      default:
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-300">
            Draft
          </span>
        );
    }
  };

  return (
    <div id="exam-management-container" className="space-y-6">
      {/* Header & Main Actions */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-zinc-200 dark:border-zinc-800 pb-5">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-zinc-900 dark:text-zinc-50">
            Examinations
          </h1>
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-1">
            Create, schedule, and administer online timed examinations.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            id="btn-auto-generate-exam"
            onClick={onAutoGenerateClick}
            className="inline-flex items-center gap-2 px-3.5 py-2 text-sm font-medium rounded-lg border border-purple-200 dark:border-purple-800/60 bg-purple-50 text-purple-700 hover:bg-purple-100 dark:bg-purple-950/30 dark:text-purple-300 dark:hover:bg-purple-900/40 transition-colors"
          >
            <Wand2 className="w-4 h-4 text-purple-600 dark:text-purple-400" />
            Auto-Generate Exam
          </button>
          <button
            id="btn-create-exam"
            onClick={onCreateClick}
            className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 shadow-sm transition-colors"
          >
            <Plus className="w-4 h-4" />
            New Examination
          </button>
        </div>
      </div>

      {/* Filters & Search */}
      <div className="grid grid-cols-1 sm:grid-cols-12 gap-3 bg-zinc-50 dark:bg-zinc-900/50 p-3.5 rounded-xl border border-zinc-200 dark:border-zinc-800">
        <form onSubmit={handleSearchSubmit} className="sm:col-span-6 relative">
          <label htmlFor={searchInputId} className="sr-only">
            Search examinations
          </label>
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-400" />
          <input
            id={searchInputId}
            type="text"
            placeholder="Search by exam title or description..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-4 py-2 text-sm rounded-lg bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100 placeholder:text-zinc-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </form>

        <div className="sm:col-span-3">
          <label htmlFor={subjectFilterId} className="sr-only">
            Filter by Subject
          </label>
          <select
            id={subjectFilterId}
            value={selectedSubject}
            onChange={(e) => setSelectedSubject(e.target.value)}
            className="w-full px-3 py-2 text-sm rounded-lg bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="">All Subjects</option>
            {subjects.map((sub) => (
              <option key={sub.id} value={sub.id}>
                {sub.code} - {sub.name}
              </option>
            ))}
          </select>
        </div>

        <div className="sm:col-span-3">
          <label htmlFor={statusFilterId} className="sr-only">
            Filter by Status
          </label>
          <select
            id={statusFilterId}
            value={selectedStatus}
            onChange={(e) => setSelectedStatus(e.target.value)}
            className="w-full px-3 py-2 text-sm rounded-lg bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="">All Statuses</option>
            <option value="draft">Draft</option>
            <option value="scheduled">Scheduled</option>
            <option value="active">Active</option>
            <option value="completed">Completed</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </div>
      </div>

      {/* Exam Cards Grid */}
      {loading ? (
        <div className="py-20 flex justify-center">
          <LoadingSpinner size="lg" />
        </div>
      ) : exams.length === 0 ? (
        <div className="text-center py-16 px-4 rounded-xl border border-dashed border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-900/30">
          <FileText className="w-12 h-12 mx-auto text-zinc-400 mb-3" />
          <h3 className="text-base font-semibold text-zinc-900 dark:text-zinc-100">
            No examinations found
          </h3>
          <p className="text-sm text-zinc-500 dark:text-zinc-400 max-w-sm mx-auto mt-1 mb-5">
            Create your first examination manually or generate one automatically from the Question Bank.
          </p>
          <div className="flex justify-center gap-3">
            <button
              onClick={onAutoGenerateClick}
              className="px-3.5 py-2 text-sm font-medium rounded-lg border border-purple-200 text-purple-700 bg-purple-50 hover:bg-purple-100 transition-colors"
            >
              Auto-Generate Exam
            </button>
            <button
              onClick={onCreateClick}
              className="px-4 py-2 text-sm font-medium rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors"
            >
              Create Examination
            </button>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {exams.map((exam) => (
            <div
              key={exam.id}
              id={`exam-card-${exam.id}`}
              className="group flex flex-col justify-between p-5 rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 hover:border-zinc-300 dark:hover:border-zinc-700 shadow-sm transition-all"
            >
              <div>
                <div className="flex items-start justify-between gap-2 mb-2.5">
                  <span className="text-xs font-semibold px-2 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300">
                    {exam.subject_code}
                  </span>
                  {getStatusBadge(exam.status)}
                </div>

                <h3 className="text-base font-bold text-zinc-900 dark:text-zinc-100 line-clamp-1 group-hover:text-indigo-600 transition-colors">
                  {exam.name}
                </h3>
                <p className="text-xs text-zinc-500 dark:text-zinc-400 line-clamp-2 mt-1 min-h-[32px]">
                  {exam.description || `Assessment for ${exam.subject_name}`}
                </p>

                <div className="grid grid-cols-2 gap-2 mt-4 pt-3 border-t border-zinc-100 dark:border-zinc-800 text-xs text-zinc-600 dark:text-zinc-300">
                  <div className="flex items-center gap-1.5">
                    <Clock className="w-3.5 h-3.5 text-zinc-400" />
                    <span>{exam.duration_minutes} Minutes</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <Award className="w-3.5 h-3.5 text-zinc-400" />
                    <span>{exam.total_marks} Marks</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <FileText className="w-3.5 h-3.5 text-zinc-400" />
                    <span>{exam.question_count} Questions</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <Users className="w-3.5 h-3.5 text-zinc-400" />
                    <span>Passing: {exam.passing_percentage}%</span>
                  </div>
                </div>

                {exam.start_date && (
                  <div className="flex items-center gap-1.5 mt-2.5 text-[11px] text-zinc-400">
                    <Calendar className="w-3 h-3" />
                    <span>Starts: {new Date(exam.start_date).toLocaleDateString()}</span>
                  </div>
                )}
              </div>

              {/* Status Controls & Action Footers */}
              <div className="mt-5 pt-3.5 border-t border-zinc-100 dark:border-zinc-800 flex items-center justify-between gap-2">
                <div className="flex items-center gap-1">
                  {exam.status === 'draft' && (
                    <button
                      disabled={actionLoading === exam.id}
                      onClick={() => handleStatusChange(exam.id, 'active')}
                      className="px-2.5 py-1 text-xs font-medium rounded bg-emerald-50 text-emerald-700 hover:bg-emerald-100 dark:bg-emerald-950/40 dark:text-emerald-300 transition-colors flex items-center gap-1"
                      title="Activate Exam"
                    >
                      <PlayCircle className="w-3.5 h-3.5" />
                      Publish & Activate
                    </button>
                  )}
                  {exam.status === 'active' && (
                    <button
                      disabled={actionLoading === exam.id}
                      onClick={() => handleStatusChange(exam.id, 'completed')}
                      className="px-2.5 py-1 text-xs font-medium rounded bg-zinc-100 text-zinc-700 hover:bg-zinc-200 dark:bg-zinc-800 dark:text-zinc-300 transition-colors flex items-center gap-1"
                      title="End Exam"
                    >
                      <CheckCircle className="w-3.5 h-3.5" />
                      End Exam
                    </button>
                  )}
                </div>

                <button
                  onClick={() => onViewResults(exam)}
                  className="px-3 py-1 text-xs font-semibold rounded bg-zinc-900 text-white dark:bg-zinc-100 dark:text-zinc-900 hover:opacity-90 transition-opacity"
                >
                  Results & Roster
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
