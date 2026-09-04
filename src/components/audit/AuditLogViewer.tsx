/**
 * ExamHub - Administrative Audit Log Viewer Component
 */

import React, { useState, useEffect } from 'react';
import { ShieldCheck, Search, Filter, Clock, User, AlertCircle } from 'lucide-react';
import { auditService } from '../../services/auditService';
import { AuditLogItem } from '../../types/audit';
import { LoadingSpinner } from '../common/LoadingSpinner';

export const AuditLogViewer: React.FC = () => {
  const [logs, setLogs] = useState<AuditLogItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionFilter, setActionFilter] = useState('');

  const fetchLogs = async () => {
    try {
      setLoading(true);
      const res = await auditService.getLogs(100, actionFilter || undefined);
      setLogs(res.items || []);
    } catch {
      setLogs([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, [actionFilter]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-zinc-200 dark:border-zinc-800 pb-4">
        <div>
          <h2 className="text-xl font-bold text-zinc-900 dark:text-zinc-50 flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-indigo-600" />
            Security Audit Trail & Compliance Records
          </h2>
          <p className="text-xs text-zinc-500 mt-0.5">
            Immutable log of all user registrations, exam publications, score overrides, and security events.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <select
            value={actionFilter}
            onChange={(e) => setActionFilter(e.target.value)}
            className="px-3 py-1.5 text-xs rounded-xl bg-white dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-800 dark:text-zinc-200"
          >
            <option value="">All Actions</option>
            <option value="GRADE_MODERATION">Grade Moderation</option>
            <option value="EXAM_CREATE">Exam Creation</option>
            <option value="USER_LOGIN">User Logins</option>
          </select>
        </div>
      </div>

      {loading ? (
        <div className="py-16 flex justify-center">
          <LoadingSpinner size="md" />
        </div>
      ) : logs.length === 0 ? (
        <div className="text-center py-12 text-zinc-400 text-xs">
          No audit records found.
        </div>
      ) : (
        <div className="bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 overflow-hidden shadow-xs">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-zinc-50 dark:bg-zinc-800/60 border-b border-zinc-200 dark:border-zinc-800 text-zinc-400 uppercase font-semibold">
                <tr>
                  <th className="py-2.5 px-4">Timestamp</th>
                  <th className="py-2.5 px-4">Action</th>
                  <th className="py-2.5 px-4">Entity</th>
                  <th className="py-2.5 px-4">Actor</th>
                  <th className="py-2.5 px-4">Details</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-100 dark:divide-zinc-800">
                {logs.map((log) => (
                  <tr key={log.id} className="hover:bg-zinc-50 dark:hover:bg-zinc-800/40 transition-colors">
                    <td className="py-2.5 px-4 font-mono text-[11px] text-zinc-400 whitespace-nowrap">
                      {log.created_at.replace('T', ' ').slice(0, 19)}
                    </td>
                    <td className="py-2.5 px-4">
                      <span className="px-2 py-0.5 rounded-full font-bold text-[10px] bg-indigo-50 text-indigo-700 dark:bg-indigo-950/40 dark:text-indigo-300">
                        {log.action}
                      </span>
                    </td>
                    <td className="py-2.5 px-4 text-zinc-600 dark:text-zinc-400">
                      {log.entity_type} {log.entity_id ? `(${log.entity_id.slice(0, 8)}...)` : ''}
                    </td>
                    <td className="py-2.5 px-4 font-medium text-zinc-800 dark:text-zinc-200">
                      {log.username || log.user_id || 'System'}
                    </td>
                    <td className="py-2.5 px-4 font-mono text-[11px] text-zinc-500 max-w-xs truncate">
                      {log.details_json}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
