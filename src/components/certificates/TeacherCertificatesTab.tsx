/**
 * ExamHub - Teacher Digital Certificate Authority & Issuance Console
 * Enables instructors to issue, inspect, and revoke cryptographically signed academic credentials.
 */

import React, { useState, useEffect } from 'react';
import {
  Award,
  Plus,
  Search,
  ExternalLink,
  ShieldCheck,
  Calendar,
  CheckCircle2,
  AlertCircle,
  Ban,
  User,
  BookOpen,
  Filter,
  Check
} from 'lucide-react';
import { CertificateRecord, CertificateIssueRequest } from '../../types/certificate';
import { certificateService } from '../../services/certificateService';
import { examService, StudentListItem } from '../../services/examService';
import { Exam } from '../../types/exam';
import { LoadingSpinner } from '../common/LoadingSpinner';
import { useToast } from '../../contexts/ToastContext';
import { CertificateViewModal } from './CertificateViewModal';

export const TeacherCertificatesTab: React.FC = () => {
  const [certificates, setCertificates] = useState<CertificateRecord[]>([]);
  const [exams, setExams] = useState<Exam[]>([]);
  const [students, setStudents] = useState<StudentListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCert, setSelectedCert] = useState<CertificateRecord | null>(null);

  // Issue modal state
  const [showIssueModal, setShowIssueModal] = useState(false);
  const [selectedExamId, setSelectedExamId] = useState('');
  const [selectedStudentId, setSelectedStudentId] = useState('');
  const [customTitle, setCustomTitle] = useState('');
  const [expiryMonths, setExpiryMonths] = useState(24);
  const [issuing, setIssuing] = useState(false);

  // Revoke state
  const [revokingCode, setRevokingCode] = useState<string | null>(null);
  const [revokeReason, setRevokeReason] = useState('Academic integrity or evaluation revision');

  const { showToast } = useToast();

  const loadData = async () => {
    try {
      setLoading(true);
      const [certRes, examsRes, studentsRes] = await Promise.all([
        certificateService.listAllCertificates().catch(() => ({ total_certificates: 0, items: [] })),
        examService.listExams({ limit: 100 }).catch(() => ({ items: [] })),
        examService.listAvailableStudents().catch(() => ({ items: [] }))
      ]);

      setCertificates(certRes.items || []);
      setExams(examsRes.items || []);
      setStudents(studentsRes.items || []);

      if (examsRes.items?.length > 0 && !selectedExamId) {
        setSelectedExamId(examsRes.items[0].id);
      }
      if (studentsRes.items?.length > 0 && !selectedStudentId) {
        setSelectedStudentId(studentsRes.items[0].student_id);
      }
    } catch (err: unknown) {
      showToast('Failed to load certificates registry', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleOpenIssueModal = () => {
    setShowIssueModal(true);
    if (exams.length > 0) {
      const e = exams[0];
      setSelectedExamId(e.id);
      setCustomTitle(`Certificate of Competence in ${e.name}`);
    }
  };

  const handleExamChange = (examId: string) => {
    setSelectedExamId(examId);
    const chosen = exams.find((e) => e.id === examId);
    if (chosen) {
      setCustomTitle(`Certificate of Competence in ${chosen.name}`);
    }
  };

  const handleIssueSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedExamId || !selectedStudentId) {
      showToast('Please select both an examination and candidate.', 'error');
      return;
    }

    try {
      setIssuing(true);
      const payload: CertificateIssueRequest = {
        exam_id: selectedExamId,
        student_id: selectedStudentId,
        custom_title: customTitle.trim() || undefined,
        expiry_months: Number(expiryMonths) || 24,
      };

      const issued = await certificateService.issueCertificate(payload);
      showToast(`Certificate ${issued.certificate_code} issued successfully!`, 'success');
      setShowIssueModal(false);
      await loadData();
    } catch (err: unknown) {
      showToast(err instanceof Error ? err.message : 'Failed to issue certificate', 'error');
    } finally {
      setIssuing(false);
    }
  };

  const handleRevoke = async () => {
    if (!revokingCode) return;
    try {
      await certificateService.revokeCertificate(revokingCode, revokeReason);
      showToast(`Certificate ${revokingCode} has been revoked.`, 'info');
      setRevokingCode(null);
      await loadData();
    } catch (err: unknown) {
      showToast(err instanceof Error ? err.message : 'Failed to revoke certificate', 'error');
    }
  };

  // Filtered Certificates
  const filteredCerts = certificates.filter((c) => {
    const q = searchQuery.toLowerCase();
    return (
      c.student_name.toLowerCase().includes(q) ||
      c.roll_number.toLowerCase().includes(q) ||
      c.exam_name.toLowerCase().includes(q) ||
      c.certificate_code.toLowerCase().includes(q)
    );
  });

  const activeCount = certificates.filter((c) => c.status === 'active').length;
  const distinctionsCount = certificates.filter((c) => c.grade === 'A+' || c.grade === 'A').length;

  if (loading) {
    return (
      <div className="py-24 flex flex-col items-center justify-center">
        <LoadingSpinner size="lg" />
        <p className="mt-3 text-xs font-semibold text-zinc-500 uppercase tracking-wider">
          Loading Academic Credential Registry...
        </p>
      </div>
    );
  }

  return (
    <div id="teacher-certificates-container" className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-zinc-200 dark:border-zinc-800 pb-5">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-zinc-900 dark:text-zinc-50 flex items-center gap-2.5">
            <Award className="w-6 h-6 text-amber-500" />
            Digital Certificate Authority & Credential Management
          </h1>
          <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">
            Issue, verify, inspect, and revoke cryptographically secured digital certificates for candidate assessments.
          </p>
        </div>

        <button
          onClick={handleOpenIssueModal}
          className="inline-flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded-xl bg-amber-600 hover:bg-amber-700 text-white shadow-xs transition-colors"
        >
          <Plus className="w-4 h-4" />
          Issue New Certificate
        </button>
      </div>

      {/* Overview Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="p-4 rounded-2xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 shadow-xs flex items-center gap-3.5">
          <div className="p-3 rounded-xl bg-amber-50 dark:bg-amber-950/40 text-amber-600">
            <Award className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs text-zinc-500 font-medium">Total Credentials</span>
            <h3 className="text-xl font-black text-zinc-900 dark:text-zinc-100">{certificates.length}</h3>
          </div>
        </div>

        <div className="p-4 rounded-2xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 shadow-xs flex items-center gap-3.5">
          <div className="p-3 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs text-zinc-500 font-medium">Active & Valid</span>
            <h3 className="text-xl font-black text-zinc-900 dark:text-zinc-100">{activeCount}</h3>
          </div>
        </div>

        <div className="p-4 rounded-2xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 shadow-xs flex items-center gap-3.5">
          <div className="p-3 rounded-xl bg-indigo-50 dark:bg-indigo-950/40 text-indigo-600">
            <CheckCircle2 className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs text-zinc-500 font-medium">Distinction Honors</span>
            <h3 className="text-xl font-black text-zinc-900 dark:text-zinc-100">{distinctionsCount}</h3>
          </div>
        </div>
      </div>

      {/* Search Bar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="relative flex-1 w-full">
          <Search className="w-4 h-4 text-zinc-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search by candidate name, roll number, exam title, or certificate code..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-4 py-2 text-xs rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 text-zinc-900 dark:text-zinc-100 placeholder:text-zinc-400 focus:outline-none focus:ring-2 focus:ring-amber-500"
          />
        </div>
        <span className="text-xs text-zinc-400 whitespace-nowrap">
          Showing {filteredCerts.length} of {certificates.length} credentials
        </span>
      </div>

      {/* Certificates Roster Table */}
      <div className="bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 overflow-hidden shadow-xs">
        {filteredCerts.length === 0 ? (
          <div className="py-16 text-center text-zinc-400 text-xs">
            <Award className="w-10 h-10 mx-auto text-zinc-400 mb-2 opacity-50" />
            <p className="font-semibold text-zinc-600 dark:text-zinc-300">No certificates matching criteria.</p>
            <p className="text-[11px] text-zinc-400 mt-1">Click "Issue New Certificate" to award credentials to passing students.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="bg-zinc-50/80 dark:bg-zinc-800/40 border-b border-zinc-200 dark:border-zinc-800 text-[11px] uppercase tracking-wider text-zinc-500 font-bold">
                  <th className="py-3 px-4">Certificate Code</th>
                  <th className="py-3 px-4">Candidate</th>
                  <th className="py-3 px-4">Examination & Subject</th>
                  <th className="py-3 px-4">Score / Grade</th>
                  <th className="py-3 px-4">Issued Date</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-100 dark:divide-zinc-800">
                {filteredCerts.map((c) => (
                  <tr key={c.id} className="hover:bg-zinc-50/60 dark:hover:bg-zinc-800/30 transition-colors">
                    <td className="py-3 px-4 font-mono font-bold text-zinc-800 dark:text-zinc-200">
                      {c.certificate_code}
                    </td>
                    <td className="py-3 px-4">
                      <div className="font-bold text-zinc-900 dark:text-zinc-100">{c.student_name}</div>
                      <span className="text-[10px] text-zinc-400 font-mono">Roll: {c.roll_number}</span>
                    </td>
                    <td className="py-3 px-4">
                      <div className="font-semibold text-zinc-800 dark:text-zinc-200">{c.exam_name}</div>
                      <span className="text-[10px] text-zinc-400">{c.subject_code} • {c.subject_name}</span>
                    </td>
                    <td className="py-3 px-4">
                      <span className="font-mono font-bold text-emerald-600 dark:text-emerald-400">
                        {c.percentage.toFixed(1)}%
                      </span>
                      <span className="ml-1.5 px-1.5 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 font-bold text-[10px] text-zinc-700 dark:text-zinc-300">
                        {c.grade}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-zinc-500">
                      {c.issue_date.slice(0, 10)}
                    </td>
                    <td className="py-3 px-4">
                      <span
                        className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                          c.status === 'active'
                            ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300'
                            : 'bg-rose-100 text-rose-800 dark:bg-rose-950/60 dark:text-rose-300'
                        }`}
                      >
                        {c.status.toUpperCase()}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => setSelectedCert(c)}
                          className="px-2.5 py-1 rounded-lg bg-amber-600 hover:bg-amber-700 text-white font-semibold text-[11px] shadow-xs transition-colors flex items-center gap-1"
                        >
                          <ExternalLink className="w-3 h-3" />
                          View
                        </button>
                        {c.status === 'active' && (
                          <button
                            onClick={() => setRevokingCode(c.certificate_code)}
                            className="px-2 py-1 rounded-lg border border-zinc-200 dark:border-zinc-700 hover:bg-rose-50 dark:hover:bg-rose-950/30 text-rose-600 dark:text-rose-400 text-[11px] font-semibold transition-colors flex items-center gap-1"
                          >
                            <Ban className="w-3 h-3" />
                            Revoke
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Issue Certificate Modal */}
      {showIssueModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs">
          <div className="w-full max-w-lg bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 shadow-2xl p-6 space-y-4">
            <div className="flex items-center gap-2.5 pb-2 border-b border-zinc-100 dark:border-zinc-800">
              <div className="p-2 rounded-xl bg-amber-100 dark:bg-amber-950/60 text-amber-600">
                <Award className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-base font-bold text-zinc-900 dark:text-zinc-100">
                  Issue Verified Digital Certificate
                </h3>
                <p className="text-xs text-zinc-500">
                  Formally award cryptographically verifiable credential to candidate.
                </p>
              </div>
            </div>

            <form onSubmit={handleIssueSubmit} className="space-y-4 text-xs">
              {/* Select Exam */}
              <div>
                <label className="block font-bold text-zinc-700 dark:text-zinc-300 mb-1">
                  Examination Assessment *
                </label>
                <select
                  value={selectedExamId}
                  onChange={(e) => handleExamChange(e.target.value)}
                  className="w-full px-3 py-2 rounded-xl bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-amber-500"
                >
                  {exams.map((ex) => (
                    <option key={ex.id} value={ex.id}>
                      {ex.name} ({ex.subject_code})
                    </option>
                  ))}
                </select>
              </div>

              {/* Select Candidate */}
              <div>
                <label className="block font-bold text-zinc-700 dark:text-zinc-300 mb-1">
                  Candidate Student *
                </label>
                <select
                  value={selectedStudentId}
                  onChange={(e) => setSelectedStudentId(e.target.value)}
                  className="w-full px-3 py-2 rounded-xl bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-amber-500"
                >
                  {students.map((st) => (
                    <option key={st.student_id} value={st.student_id}>
                      {st.full_name} (Roll: {st.student_id_code})
                    </option>
                  ))}
                </select>
              </div>

              {/* Certificate Title */}
              <div>
                <label className="block font-bold text-zinc-700 dark:text-zinc-300 mb-1">
                  Official Certificate Title
                </label>
                <input
                  type="text"
                  value={customTitle}
                  onChange={(e) => setCustomTitle(e.target.value)}
                  placeholder="e.g. Certificate of Competence in DBMS & SQL Proficiency"
                  className="w-full px-3 py-2 rounded-xl bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-amber-500"
                />
              </div>

              {/* Expiry Months */}
              <div>
                <label className="block font-bold text-zinc-700 dark:text-zinc-300 mb-1">
                  Credential Validity (Months)
                </label>
                <input
                  type="number"
                  min="1"
                  max="120"
                  value={expiryMonths}
                  onChange={(e) => setExpiryMonths(Number(e.target.value))}
                  className="w-full px-3 py-2 rounded-xl bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-amber-500"
                />
              </div>

              {/* Preview Notice */}
              <div className="p-3 rounded-xl bg-amber-50/60 dark:bg-amber-950/20 border border-amber-200/60 dark:border-amber-900/40 text-[11px] text-amber-900 dark:text-amber-200 leading-normal">
                Upon issuing, the system signs the record using SHA-256 and computes a unique verification hash. The student will immediately see this credential under "My Certificates".
              </div>

              {/* Actions */}
              <div className="flex items-center justify-end gap-2 pt-2 border-t border-zinc-100 dark:border-zinc-800">
                <button
                  type="button"
                  onClick={() => setShowIssueModal(false)}
                  className="px-4 py-2 rounded-xl border border-zinc-200 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300 hover:bg-zinc-50 dark:hover:bg-zinc-800 font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={issuing}
                  className="px-4 py-2 rounded-xl bg-amber-600 hover:bg-amber-700 text-white font-semibold flex items-center gap-1.5 shadow-xs disabled:opacity-50"
                >
                  {issuing && <LoadingSpinner size="sm" />}
                  Issue & Digitally Sign Certificate
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Revocation Confirmation Modal */}
      {revokingCode && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs">
          <div className="w-full max-w-md bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 shadow-2xl p-6 space-y-4">
            <div className="flex items-center gap-2.5 text-rose-600">
              <Ban className="w-5 h-5" />
              <h3 className="text-base font-bold">Confirm Credential Revocation</h3>
            </div>
            <p className="text-xs text-zinc-500">
              Are you sure you want to revoke certificate <strong className="font-mono">{revokingCode}</strong>? This cannot be undone and will invalidate public verification.
            </p>

            <div>
              <label className="block text-xs font-bold text-zinc-700 dark:text-zinc-300 mb-1">
                Reason for Revocation
              </label>
              <input
                type="text"
                value={revokeReason}
                onChange={(e) => setRevokeReason(e.target.value)}
                className="w-full px-3 py-2 text-xs rounded-xl bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100"
              />
            </div>

            <div className="flex justify-end gap-2 pt-2">
              <button
                type="button"
                onClick={() => setRevokingCode(null)}
                className="px-3.5 py-2 text-xs rounded-xl border border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-300 font-semibold"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleRevoke}
                className="px-4 py-2 text-xs rounded-xl bg-rose-600 hover:bg-rose-700 text-white font-semibold shadow-xs"
              >
                Confirm Revocation
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Full Certificate View/Print Modal */}
      {selectedCert && (
        <CertificateViewModal
          certificate={selectedCert}
          isOpen={Boolean(selectedCert)}
          onClose={() => setSelectedCert(null)}
        />
      )}
    </div>
  );
};
