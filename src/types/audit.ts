/**
 * ExamHub - Audit Trail Interfaces
 */

export interface AuditLogItem {
  id: string;
  user_id?: string;
  username?: string;
  action: string;
  entity_type: string;
  entity_id?: string;
  details_json?: string;
  created_at: string;
}

export interface AuditLogsListResponse {
  total_records: number;
  items: AuditLogItem[];
}
