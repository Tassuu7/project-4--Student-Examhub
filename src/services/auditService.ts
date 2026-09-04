/**
 * ExamHub - Audit Trail Service
 */

import { api } from './apiClient';
import { AuditLogsListResponse } from '../types/audit';

export const auditService = {
  getLogs: (limit: number = 100, action?: string): Promise<AuditLogsListResponse> => {
    const params = new URLSearchParams();
    params.set('limit', limit.toString());
    if (action) params.set('action', action);
    return api.get<AuditLogsListResponse>(`/audit/logs?${params.toString()}`);
  },
};
