/**
 * ExamHub - Certificate View Modal Component
 * Displays a verifiable certificate with print styling and download controls.
 */

import React from 'react';
import { Award, CheckCircle, Printer, X, ShieldCheck, ExternalLink } from 'lucide-react';
import { CertificateRecord } from '../../types/certificate';

interface CertificateViewModalProps {
  certificate: CertificateRecord | null;
  isOpen: boolean;
  onClose: () => void;
}

export const CertificateViewModal: React.FC<CertificateViewModalProps> = ({
  certificate,
  isOpen,
  onClose,
}) => {
  if (!isOpen || !certificate) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs">
      <div className="w-full max-w-2xl bg-white dark:bg-zinc-900 rounded-3xl shadow-2xl border border-zinc-200 dark:border-zinc-800 overflow-hidden flex flex-col max-h-[90vh]">
        {/* Modal Header */}
        <div className="flex items-center justify-between p-4 px-6 border-b border-zinc-100 dark:border-zinc-800">
          <div className="flex items-center gap-2">
            <Award className="w-5 h-5 text-amber-500" />
            <h2 className="text-sm font-bold text-zinc-900 dark:text-zinc-100">
              Verified Academic Credential
            </h2>
          </div>
          <button
            onClick={onClose}
            className="p-1 text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-200 rounded-lg"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Certificate Body Container */}
        <div className="p-6 overflow-y-auto">
          <div className="p-8 border-4 border-double border-amber-600/60 rounded-2xl bg-amber-50/20 dark:bg-zinc-950 text-center space-y-4">
            <div className="text-2xl text-amber-600">&#10022; &#10022; &#10022;</div>
            <p className="text-[11px] uppercase tracking-widest text-zinc-500 font-bold">
              ExamHub Certification Board
            </p>
            <h1 className="text-2xl font-black text-zinc-900 dark:text-zinc-50 tracking-tight">
              Certificate of Achievement
            </h1>
            <p className="text-xs text-zinc-500 italic">This is formally conferred upon</p>

            <div className="py-2">
              <span className="text-xl font-bold text-amber-700 dark:text-amber-400 border-b-2 border-zinc-300 dark:border-zinc-700 pb-1 px-8 inline-block">
                {certificate.student_name}
              </span>
              <p className="text-[11px] text-zinc-400 mt-1 font-mono">
                Roll No: {certificate.roll_number}
              </p>
            </div>

            <p className="text-xs text-zinc-700 dark:text-zinc-300 max-w-md mx-auto leading-relaxed">
              For demonstrating competence and successfully passing the proctored assessment for{' '}
              <strong className="text-zinc-900 dark:text-zinc-100">{certificate.exam_name}</strong> ({certificate.subject_code} &mdash; {certificate.subject_name}).
            </p>

            <div className="flex justify-center gap-4 py-2 text-xs">
              <div className="px-3 py-1 rounded-lg bg-zinc-100 dark:bg-zinc-800 font-semibold">
                Grade: <span className="text-indigo-600 dark:text-indigo-400">{certificate.grade}</span>
              </div>
              <div className="px-3 py-1 rounded-lg bg-zinc-100 dark:bg-zinc-800 font-semibold">
                Score: <span className="text-emerald-600 dark:text-emerald-400">{certificate.percentage.toFixed(1)}%</span>
              </div>
              <div className="px-3 py-1 rounded-lg bg-zinc-100 dark:bg-zinc-800 font-semibold">
                Issued: {certificate.issue_date.slice(0, 10)}
              </div>
            </div>

            <div className="pt-4 border-t border-zinc-200 dark:border-zinc-800 flex items-center justify-between text-[11px] text-zinc-400 font-mono">
              <div className="flex items-center gap-1 text-emerald-600 dark:text-emerald-400 font-semibold">
                <ShieldCheck className="w-4 h-4" /> Cryptographically Verified
              </div>
              <div>ID: {certificate.certificate_code}</div>
            </div>
          </div>
        </div>

        {/* Footer Actions */}
        <div className="p-4 px-6 border-t border-zinc-100 dark:border-zinc-800 flex justify-end gap-2 bg-zinc-50 dark:bg-zinc-800/40">
          <a
            href={`/api/v1/certificates/render/${certificate.certificate_code}`}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 px-4 py-2 text-xs font-semibold rounded-xl bg-amber-600 text-white hover:bg-amber-700 shadow-sm transition-colors"
          >
            <Printer className="w-3.5 h-3.5" />
            Official Printable Layout
          </a>
        </div>
      </div>
    </div>
  );
};
