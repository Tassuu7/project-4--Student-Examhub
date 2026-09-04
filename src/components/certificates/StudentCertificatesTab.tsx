/**
 * ExamHub - Student Earned Certificates Tab
 * Allows students to view and inspect all awarded certificates.
 */

import React, { useState, useEffect } from 'react';
import { Award, ExternalLink, Calendar, CheckCircle2 } from 'lucide-react';
import { CertificateRecord } from '../../types/certificate';
import { certificateService } from '../../services/certificateService';
import { useAuth } from '../../contexts/AuthContext';
import { LoadingSpinner } from '../common/LoadingSpinner';
import { CertificateViewModal } from './CertificateViewModal';

export const StudentCertificatesTab: React.FC = () => {
  const { user } = useAuth();
  const [certificates, setCertificates] = useState<CertificateRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCert, setSelectedCert] = useState<CertificateRecord | null>(null);

  useEffect(() => {
    if (!user || !user.student_id) return;
    const fetchCerts = async () => {
      try {
        setLoading(true);
        const res = await certificateService.getStudentCertificates(user.student_id!);
        setCertificates(res.items || []);
      } catch {
        setCertificates([]);
      } finally {
        setLoading(false);
      }
    };
    fetchCerts();
  }, [user]);

  if (loading) {
    return (
      <div className="py-16 flex justify-center">
        <LoadingSpinner size="md" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="border-b border-zinc-200 dark:border-zinc-800 pb-4">
        <h2 className="text-xl font-bold text-zinc-900 dark:text-zinc-50 flex items-center gap-2">
          <Award className="w-5 h-5 text-amber-500" />
          My Earned Academic Credentials
        </h2>
        <p className="text-xs text-zinc-500 mt-1">
          Certificates formally issued for successfully completed assessments.
        </p>
      </div>

      {certificates.length === 0 ? (
        <div className="text-center py-16 px-4 rounded-2xl border border-dashed border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-900">
          <Award className="w-10 h-10 mx-auto text-zinc-400 mb-2" />
          <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">
            No certificates earned yet
          </h3>
          <p className="text-xs text-zinc-500 max-w-sm mx-auto mt-1">
            Complete and achieve a passing score in your assigned examinations to be awarded verified certificates.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {certificates.map((cert) => (
            <div
              key={cert.id}
              className="p-5 rounded-2xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 shadow-xs hover:border-amber-400 dark:hover:border-amber-600 transition-all flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between gap-2 mb-2">
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-amber-50 text-amber-700 dark:bg-amber-950/40 dark:text-amber-300">
                    {cert.subject_code}
                  </span>
                  <span className="text-[11px] font-mono text-zinc-400">
                    {cert.certificate_code}
                  </span>
                </div>
                <h3 className="text-base font-bold text-zinc-900 dark:text-zinc-100">
                  {cert.exam_name}
                </h3>
                <p className="text-xs text-zinc-500 mt-0.5">
                  {cert.subject_name}
                </p>

                <div className="flex items-center gap-4 mt-3 pt-3 border-t border-zinc-100 dark:border-zinc-800 text-xs">
                  <div>
                    <span className="text-zinc-400 text-[10px] block">Score</span>
                    <strong className="text-emerald-600 font-bold">{cert.percentage.toFixed(1)}% ({cert.grade})</strong>
                  </div>
                  <div>
                    <span className="text-zinc-400 text-[10px] block">Issued</span>
                    <strong className="text-zinc-700 dark:text-zinc-300">{cert.issue_date.slice(0, 10)}</strong>
                  </div>
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-zinc-100 dark:border-zinc-800 flex justify-end">
                <button
                  onClick={() => setSelectedCert(cert)}
                  className="px-3.5 py-1.5 rounded-xl bg-amber-600 hover:bg-amber-700 text-white font-semibold text-xs shadow-xs transition-colors flex items-center gap-1.5"
                >
                  <ExternalLink className="w-3.5 h-3.5" />
                  View & Print Certificate
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

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
