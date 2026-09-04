/**
 * ExamHub - Exam Engine & Attempt TypeScript Types
 */

export type ExamStatus = 'draft' | 'scheduled' | 'active' | 'completed' | 'cancelled';
export type AttemptStatus = 'not_started' | 'in_progress' | 'submitted' | 'auto_submitted' | 'evaluated' | 'disqualified';

export interface ExamAssignedStudent {
  assignment_id: string;
  assigned_at: string;
  can_attempt: boolean;
  student_id: string;
  student_roll_number: string;
  grade_level?: string;
  user_id: string;
  full_name: string;
  email: string;
  attempt_id?: string;
  attempt_status?: AttemptStatus;
  obtained_marks?: number;
  percentage?: number;
  grade?: string;
  pass_fail?: 'PASS' | 'FAIL';
}

export interface ExamQuestionAllocation {
  exam_question_id: string;
  question_id: string;
  order_index: number;
  marks_allocated: number;
  question_text: string;
  option_a: string;
  option_b: string;
  option_c: string;
  option_d: string;
  difficulty: string;
  topic?: string;
  correct_answer?: string;
  explanation?: string;
}

export interface Exam {
  id: string;
  name: string;
  subject_id: string;
  subject_code: string;
  subject_name: string;
  teacher_id: string;
  teacher_name: string;
  description?: string;
  duration_minutes: number;
  total_marks: number;
  passing_percentage: number;
  start_date: string;
  end_date: string;
  instructions?: string;
  status: ExamStatus;
  question_count: number;
  assigned_count?: number;
  questions?: ExamQuestionAllocation[];
  assigned_students?: ExamAssignedStudent[];
  created_at: string;
  updated_at: string;
}

export interface StudentPortalExam extends Exam {
  can_attempt: boolean;
  attempts_allowed: number;
  attempt_id?: string;
  attempt_status?: AttemptStatus;
  time_remaining_seconds?: number;
  start_time?: string;
  end_time?: string;
  obtained_marks?: number;
  percentage?: number;
  grade?: string;
  pass_fail?: 'PASS' | 'FAIL';
  rank?: number;
}

export interface ExamAttemptQuestion {
  id: string;
  question_id: string;
  order_index: number;
  question_text: string;
  option_a: string;
  option_b: string;
  option_c: string;
  option_d: string;
  marks_allocated: number;
  difficulty: string;
  topic?: string;
  selected_option?: 'A' | 'B' | 'C' | 'D' | null;
  is_marked_for_review: boolean;
}

export interface ExamAttemptStartResponse {
  attempt_id: string;
  exam_id: string;
  exam_name: string;
  subject_code: string;
  subject_name: string;
  duration_minutes: number;
  time_remaining_seconds: number;
  start_time: string;
  status: AttemptStatus;
  questions: ExamAttemptQuestion[];
  instructions?: string;
}

export interface ReviewItem {
  question_id: string;
  order_index: number;
  question_text: string;
  option_a: string;
  option_b: string;
  option_c: string;
  option_d: string;
  selected_option?: string | null;
  correct_answer: string;
  is_correct: boolean;
  marks_allocated: number;
  marks_obtained: number;
  explanation?: string | null;
  topic?: string | null;
  difficulty: string;
}

export interface ExamResult {
  result_id: string;
  attempt_id: string;
  exam_id: string;
  exam_name: string;
  subject_code: string;
  subject_name: string;
  student_id: string;
  student_name: string;
  student_roll_number: string;
  total_questions: number;
  correct_count: number;
  wrong_count: number;
  unanswered_count: number;
  total_marks: number;
  obtained_marks: number;
  percentage: number;
  grade: string;
  pass_fail: 'PASS' | 'FAIL';
  rank?: number | null;
  total_candidates: number;
  start_time?: string;
  end_time?: string;
  generated_at: string;
  review_items: ReviewItem[];
}

export interface ProctoringEvent {
  event_type: 'tab_switch' | 'fullscreen_exit' | 'blur' | 'copy_paste' | 'suspicious_key';
  details?: string;
  timestamp?: string;
}

export interface IntegritySummary {
  attempt_id: string;
  student_name: string;
  student_roll_number: string;
  exam_name: string;
  total_events: number;
  tab_switches: number;
  fullscreen_exits: number;
  window_blurs: number;
  copy_pastes: number;
  suspicious_keys: number;
  events: Array<{
    id: string;
    event_type: string;
    details?: string;
    timestamp: string;
  }>;
}

export interface ExamCreateFormData {
  name: string;
  subject_id: string;
  description?: string;
  duration_minutes: number;
  passing_percentage: number;
  start_date: string;
  end_date: string;
  instructions?: string;
  question_ids: string[];
  student_ids: string[];
}

export interface ExamAutoGenerateFormData {
  subject_id: string;
  name: string;
  duration_minutes: number;
  passing_percentage: number;
  start_date: string;
  end_date: string;
  easy_count: number;
  medium_count: number;
  hard_count: number;
  topic_filter?: string;
  instructions?: string;
}
