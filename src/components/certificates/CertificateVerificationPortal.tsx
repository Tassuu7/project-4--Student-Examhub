/**
 * ExamHub - Public Certificate Verification Portal
 * Verifies certificate codes and displays cryptographic validity.
 */

import React, { useState } from 'react';
import { Search, ShieldCheck, ShieldAlert, Award } from 'lucide-react';
import { certificateService } from '../../services/certificateService';
import { CertificateVerificationResponse } from '../../types/certificate';
import { LoadingSpinner } from '../common/LoadingSpinner';

export const CertificateVerificationPortal: React.FC = () => {
  const [code, setCode] = useState('');
  const [result, setResult] = useState<CertificateVerificationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const handleVerify = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!code.trim()) return;

    try {
      setLoading(true);
      setSearched(true);
      const res = await certificateService.verifyCertificate(code.trim());
      setResult(res);
    } catch {
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="text-center space-y-2">
        <div className="w-12 h-12 rounded-2xl bg-amber-100 dark:bg-amber-950/40 text-amber-600 flex items-center justify-center mx-auto shadow-xs">
          <Award className="w-6 h-6" />
        </div>
        <h1 className="text-2xl font-bold text-zinc-900 dark:text-zinc-50">
          Academic Credential Verification
        </h1>
        <p className="text-xs text-zinc-500 max-w-md mx-auto">
          Enter an ExamHub Certificate Serial Code to verify authenticity and inspect academic grading records.
        </p>
      </div>

      <form onSubmit={handleVerify} className="flex gap-2">
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-zinc-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="e.g. EXAM-A7B2-9F1C-2026"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-sm font-mono focus:ring-2 focus:ring-amber-500 focus:outline-none"
          />
        </div>
        <button
          type="submit"
          disabled={loading || !code.trim()}
          className="px-5 py-2.5 rounded-xl bg-amber-600 text-white font-semibold text-xs shadow-xs hover:bg-amber-700 disabled:opacity-50 transition-colors"
        >
          {loading ? <LoadingSpinner size="sm" /> : 'Verify Code'}
        </button>
      </form>

      {searched && !loading && (
        <div>
          {result && result.is_valid ? (
            <div className="p-6 rounded-2xl border border-emerald-200 bg-emerald-50/40 dark:bg-emerald-950/20 dark:border-emerald-800/50 space-y-3">
              <div className="flex items-center gap-2 text-emerald-800 dark:text-emerald-300 font-bold text-sm">
                <ShieldCheck className="w-5 h-5 text-emerald-600" />
                Verified Authentic Academic Credential
              </div>
              <div className="grid grid-cols-2 gap-3 text-xs pt-2 border-t border-emerald-200/60 dark:border-emerald-800/40">
                <div>
                  <span className="text-zinc-500 block">Candidate Name:</span>
                  <strong className="text-zinc-900 dark:text-zinc-100">{result.student_name}</strong>
                </div>
                <div>
                  <span className="text-zinc-500 block">Roll Number:</span>
                  <strong className="text-zinc-900 dark:text-zinc-100">{result.roll_number}</strong>
                </div>
                <div>
                  <span className="text-zinc-500 block">Examination:</span>
                  <strong className="text-zinc-900 dark:text-zinc-100">{result.exam_name}</strong>
                </div>
                <div>
                  <span className="text-zinc-500 block">Subject:</span>
                  <strong className="text-zinc-900 dark:text-zinc-100">{result.subject_code} &mdash; {result.subject_name}</strong>
                </div>
                <div>
                  <span className="text-zinc-500 block">Grade & Score:</span>
                  <strong className="text-emerald-700 dark:text-emerald-300">{result.grade} ({result.percentage.toFixed(1)}%)</strong>
                </div>
                <div>
                  <span className="text-zinc-500 block">Issue Date:</span>
                  <strong className="text-zinc-900 dark:text-zinc-100">{result.issue_date.slice(0, 10)}</strong>
                </div>
              </div>
            </div>
          ) : (
            <div className="p-6 rounded-2xl border border-rose-200 bg-rose-50/40 dark:bg-rose-950/20 dark:border-rose-800/50 text-center space-y-2">
              <ShieldAlert className="w-6 h-6 text-rose-600 mx-auto" />
              <h3 className="text-sm font-bold text-rose-900 dark:text-rose-200">
                Invalid or Unverified Credential
              </h3>
              <p className="text-xs text-rose-700 dark:text-rose-300">
                The certificate serial was not found or has been revoked by the issuing board.
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
