import React, { useState } from 'react';
import { QuestionService } from '@/src/services/questionService.ts';
import { BulkImportResult } from '@/src/types/question.ts';
import { useToast } from '@/src/contexts/ToastContext.tsx';
import { X, Upload, Download, CheckCircle, AlertTriangle } from 'lucide-react';
import { LoadingSpinner } from '@/src/components/common/LoadingSpinner.tsx';

interface QuestionBulkImportModalProps {
  isOpen: boolean;
  onClose: () => void;
  onImportSuccess: () => void;
}

export const QuestionBulkImportModal: React.FC<QuestionBulkImportModalProps> = ({
  isOpen,
  onClose,
  onImportSuccess,
}) => {
  const { showSuccess, showError } = useToast();
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<BulkImportResult | null>(null);

  if (!isOpen) return null;

  const handleDownloadTemplate = async () => {
    try {
      const blob = await QuestionService.downloadTemplate();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'examhub_questions_template.csv';
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch {
      showError('Failed to download CSV template.');
    }
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      showError('Please select a valid .csv file.');
      return;
    }

    setUploading(true);
    setResult(null);
    try {
      const res = await QuestionService.importCsv(file);
      setResult(res);
      if (res.imported_count > 0) {
        showSuccess(`Successfully imported ${res.imported_count} questions.`);
        onImportSuccess();
      } else {
        showError('No questions could be imported. Please review the errors below.');
      }
    } catch (err: unknown) {
      showError(err instanceof Error ? err.message : 'Import failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div id="bulk-import-modal-overlay" className="fixed inset-0 z-50 bg-stone-900/50 backdrop-blur-xs flex items-center justify-center p-4">
      <div id="bulk-import-modal-container" className="bg-white rounded-xl shadow-xl border border-stone-200 w-full max-w-lg overflow-hidden">
        <div className="flex items-center justify-between px-6 py-4 border-b border-stone-200 bg-stone-50">
          <div>
            <h3 className="text-base font-semibold text-stone-900">Bulk Import Questions</h3>
            <p className="text-xs text-stone-500">Upload multiple-choice questions from a standard CSV file</p>
          </div>
          <button
            id="close-bulk-import-modal-btn"
            onClick={onClose}
            className="text-stone-400 hover:text-stone-700 p-1 rounded-md transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6 space-y-5">
          <div className="flex items-center justify-between p-3.5 bg-stone-50 rounded-lg border border-stone-200">
            <div>
              <p className="text-xs font-semibold text-stone-800">CSV Template</p>
              <p className="text-[11px] text-stone-500">Download the required columns and sample format</p>
            </div>
            <button
              id="download-csv-template-btn"
              type="button"
              onClick={handleDownloadTemplate}
              className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-stone-700 bg-white hover:bg-stone-100 border border-stone-300 rounded-md transition-colors"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Download Template</span>
            </button>
          </div>

          <form onSubmit={handleUpload} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-stone-700 mb-1.5">Select CSV File</label>
              <input
                id="csv-file-input"
                type="file"
                accept=".csv"
                onChange={(e) => {
                  setFile(e.target.files?.[0] || null);
                  setResult(null);
                }}
                className="block w-full text-xs text-stone-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-xs file:font-semibold file:bg-amber-50 file:text-amber-700 hover:file:bg-amber-100"
              />
            </div>

            <button
              id="upload-csv-submit-btn"
              type="submit"
              disabled={uploading || !file}
              className="w-full flex items-center justify-center gap-2 py-2.5 px-4 bg-amber-600 hover:bg-amber-700 text-white font-medium text-xs rounded-lg transition-colors disabled:opacity-50"
            >
              {uploading ? (
                <LoadingSpinner size="sm" />
              ) : (
                <>
                  <Upload className="w-4 h-4" />
                  <span>Start Import</span>
                </>
              )}
            </button>
          </form>

          {result && (
            <div id="import-results-container" className="p-4 rounded-lg bg-stone-50 border border-stone-200 space-y-2 text-xs">
              <div className="flex items-center gap-2">
                <CheckCircle className="w-4 h-4 text-emerald-600" />
                <span className="font-semibold text-stone-800">Processed: {result.total_processed} rows</span>
              </div>
              <div className="text-emerald-700">Successfully imported: {result.imported_count} questions</div>
              {result.failed_count > 0 && (
                <div className="space-y-1 pt-2 border-t border-stone-200">
                  <div className="flex items-center gap-1.5 text-rose-700 font-semibold">
                    <AlertTriangle className="w-3.5 h-3.5" />
                    <span>Failed rows ({result.failed_count}):</span>
                  </div>
                  <ul className="list-disc pl-5 text-rose-600 space-y-0.5 max-h-32 overflow-y-auto">
                    {result.errors.map((err, i) => (
                      <li key={i}>{err}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
