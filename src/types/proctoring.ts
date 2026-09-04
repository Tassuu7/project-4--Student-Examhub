/**
 * ExamHub - Proctoring & Security Telemetry Interfaces
 */

export interface ProctoringEventItem {
  id: string;
  attempt_id: string;
  event_type: string;
  details?: string;
  timestamp: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
}

export interface CandidateIntegrityProfile {
  attempt_id: string;
  student_id: string;
  student_name: string;
  roll_number: string;
  exam_id: string;
  exam_name: string;
  integrity_score: number;
  risk_level: 'Normal' | 'Moderate' | 'High' | 'Severe';
  total_anomalies: number;
  tab_switch_count: number;
  blur_count: number;
  audio_spike_count: number;
  face_anomalies_count: number;
  devtools_attempts_count: number;
  is_flagged_for_manual_review: boolean;
  events: ProctoringEventItem[];
}

export interface ActiveSessionMonitoringItem {
  attempt_id: string;
  student_name: string;
  roll_number: string;
  exam_name: string;
  time_remaining_seconds: number;
  current_status: string;
  last_ping: string;
  integrity_score: number;
  total_warnings: number;
}

export interface ProctoringLiveFeedResponse {
  active_sessions_count: number;
  flagged_sessions_count: number;
  active_candidates: ActiveSessionMonitoringItem[];
  recent_events: ProctoringEventItem[];
}
