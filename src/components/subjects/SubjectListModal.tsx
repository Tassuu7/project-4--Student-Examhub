import React, { useState, useEffect } from 'react';
import { Subject, SubjectFormData } from '@/src/types/subject.ts';
import { SubjectService } from '@/src/services/subjectService.ts';
import { useToast } from '@/src/contexts/ToastContext.tsx';
import { X, Plus, BookOpen, Search, Check } from 'lucide-react';
import { LoadingSpinner } from '@/src/components/common/LoadingSpinner.tsx';

interface SubjectListModalProps {
  isOpen: boolean;
  onClose: () => void;
  isAdmin?: boolean;
}

export const SubjectListModal: React.FC<SubjectListModalProps> = ({
  isOpen,
  onClose,
  isAdmin = false,
}) => {
  const { showSuccess, showError } = useToast();
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState('');
  const [isAdding, setIsAdding] = useState(false);
  const [newSubject, setNewSubject] = useState<SubjectFormData>({
    code: '',
    name: '',
    description: '',
    department: '',
  });

  useEffect(() => {
    if (isOpen) {
      loadSubjects();
    }
  }, [isOpen]);

  const loadSubjects = async () => {
    setLoading(true);
    try {
      const res = await SubjectService.listSubjects(search || undefined);
      setSubjects(res.items);
    } catch {
      showError('Failed to load academic subjects');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  const handleCreateSubject = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newSubject.code.trim() || !newSubject.name.trim()) {
      showError('Subject code and title are required.');
      return;
    }

    try {
      await SubjectService.createSubject(newSubject);
      showSuccess(`Subject ${newSubject.code} created.`);
      setIsAdding(false);
      setNewSubject({ code: '', name: '', description: '', department: '' });
      loadSubjects();
    } catch (err: unknown) {
      showError(err instanceof Error ? err.message : 'Failed to create subject.');
    }
  };

  return (
    <div id="subject-modal-overlay" className="fixed inset-0 z-50 bg-stone-900/50 backdrop-blur-xs flex items-center justify-center p-4">
      <div id="subject-modal-container" className="bg-white rounded-xl shadow-xl border border-stone-200 w-full max-w-2xl max-h-[85vh] flex flex-col overflow-hidden">
        <div className="flex items-center justify-between px-6 py-4 border-b border-stone-200 bg-stone-50 shrink-0">
          <div className="flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-amber-600" />
            <div>
              <h3 className="text-base font-semibold text-stone-900">Academic Subjects Catalog</h3>
              <p className="text-xs text-stone-500">Curriculum subjects and question repository breakdown</p>
            </div>
          </div>
          <button
            id="close-subject-modal-btn"
            onClick={onClose}
            className="text-stone-400 hover:text-stone-700 p-1 rounded-md transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6 flex-1 overflow-y-auto space-y-4">
          <div className="flex items-center justify-between gap-3">
            <div className="relative flex-1">
              <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-stone-400" />
              <input
                id="subject-search-input"
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && loadSubjects()}
                placeholder="Search subjects by code, title..."
                className="w-full pl-9 pr-3 py-2 text-xs bg-stone-50 border border-stone-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:bg-white"
              />
            </div>
            {isAdmin && !isAdding && (
              <button
                id="add-new-subject-btn"
                onClick={() => setIsAdding(true)}
                className="flex items-center gap-1.5 px-3 py-2 text-xs font-medium text-white bg-amber-600 hover:bg-amber-700 rounded-lg shadow-sm transition-colors"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>New Subject</span>
              </button>
            )}
          </div>

          {isAdding && (
            <form onSubmit={handleCreateSubject} className="p-4 bg-amber-50/50 border border-amber-200 rounded-lg space-y-3">
              <h4 className="text-xs font-bold text-stone-800 uppercase tracking-wider">Create New Subject</h4>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-[11px] font-semibold text-stone-700 mb-1">Subject Code</label>
                  <input
                    type="text"
                    required
                    value={newSubject.code}
                    onChange={(e) => setNewSubject({ ...newSubject, code: e.target.value.toUpperCase() })}
                    placeholder="e.g. CS305"
                    className="w-full px-2.5 py-1.5 text-xs bg-white border border-stone-300 rounded-md focus:ring-1 focus:ring-amber-500"
                  />
                </div>
                <div>
                  <label className="block text-[11px] font-semibold text-stone-700 mb-1">Department</label>
                  <input
                    type="text"
                    value={newSubject.department}
                    onChange={(e) => setNewSubject({ ...newSubject, department: e.target.value })}
                    placeholder="e.g. Computer Science"
                    className="w-full px-2.5 py-1.5 text-xs bg-white border border-stone-300 rounded-md focus:ring-1 focus:ring-amber-500"
                  />
                </div>
              </div>
              <div>
                <label className="block text-[11px] font-semibold text-stone-700 mb-1">Subject Title</label>
                <input
                  type="text"
                  required
                  value={newSubject.name}
                  onChange={(e) => setNewSubject({ ...newSubject, name: e.target.value })}
                  placeholder="e.g. Advanced Operating Systems"
                  className="w-full px-2.5 py-1.5 text-xs bg-white border border-stone-300 rounded-md focus:ring-1 focus:ring-amber-500"
                />
              </div>
              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setIsAdding(false)}
                  className="px-3 py-1.5 text-xs text-stone-600 hover:bg-stone-100 rounded-md"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex items-center gap-1 px-3 py-1.5 text-xs font-medium text-white bg-amber-600 hover:bg-amber-700 rounded-md"
                >
                  <Check className="w-3.5 h-3.5" />
                  <span>Save Subject</span>
                </button>
              </div>
            </form>
          )}

          {loading ? (
            <LoadingSpinner size="md" label="Loading curriculum subjects..." />
          ) : (
            <div className="divide-y divide-stone-200 border border-stone-200 rounded-lg overflow-hidden">
              {subjects.map((sub) => (
                <div key={sub.id} className="p-4 bg-white hover:bg-stone-50/50 transition-colors flex items-center justify-between">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs font-bold px-2 py-0.5 rounded bg-stone-100 text-stone-800 border border-stone-200">
                        {sub.code}
                      </span>
                      <h4 className="text-sm font-semibold text-stone-900">{sub.name}</h4>
                    </div>
                    {sub.description && <p className="text-xs text-stone-500 mt-1 line-clamp-1">{sub.description}</p>}
                    <div className="flex items-center gap-3 mt-2 text-[11px] text-stone-500">
                      <span>Department: {sub.department || 'General'}</span>
                      <span>•</span>
                      <span>Questions: <strong className="text-stone-700">{sub.question_count}</strong></span>
                      <span>•</span>
                      <span>Exams: <strong className="text-stone-700">{sub.exam_count}</strong></span>
                    </div>
                  </div>
                </div>
              ))}
              {subjects.length === 0 && (
                <div className="p-8 text-center text-xs text-stone-400">No subjects matching your criteria</div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
