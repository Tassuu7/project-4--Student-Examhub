/**
 * ExamHub - Analytics & Psychometrics TypeScript Interfaces
 */

export interface ScoreSummary {
  total_candidates: number;
  evaluated_candidates: number;
  mean_score: number;
  median_score: number;
  mode_score: number | null;
  standard_deviation: number;
  variance: number;
  minimum_score: number;
  maximum_score: number;
  range_score: number;
  q1_score: number;
  q3_score: number;
  iqr_score: number;
  skewness: number;
  kurtosis: number;
}

export interface GradeBucket {
  grade: string;
  count: number;
  percentage: number;
  min_score: number;
  max_score: number;
  color_code: string;
}

export interface PassFailMetrics {
  total_appeared: number;
  passed_count: number;
  failed_count: number;
  passing_percentage: number;
  pass_rate: number;
  fail_rate: number;
  threshold_marks: number;
}

export interface QuestionItemMetric {
  question_id: string;
  order_index: number;
  question_text: string;
  difficulty_assigned: string;
  topic?: string;
  marks_allocated: number;
  total_attempts: number;
  correct_attempts: number;
  wrong_attempts: number;
  unanswered_attempts: number;
  facility_index: number;
  discrimination_index: number;
  point_biserial: number;
  discrimination_status: string;
  option_a_selection_rate: number;
  option_b_selection_rate: number;
  option_c_selection_rate: number;
  option_d_selection_rate: number;
  average_time_seconds?: number;
}

export interface TopicPerformance {
  topic: string;
  question_count: number;
  total_marks: number;
  average_accuracy_percentage: number;
  mastery_level: 'Mastered' | 'Proficient' | 'Developing' | 'Novice';
  weak_student_count: number;
  strong_student_count: number;
}

export interface CandidateRankItem {
  rank: number;
  student_id: string;
  user_id: string;
  full_name: string;
  roll_number: string;
  obtained_marks: number;
  total_marks: number;
  percentage: number;
  grade: string;
  pass_fail: 'PASS' | 'FAIL';
  percentile: number;
  completion_time_seconds: number;
  time_taken_formatted: string;
  submitted_at: string;
}

export interface DecileDistribution {
  decile: string;
  lower_bound: number;
  upper_bound: number;
  student_count: number;
  percentage_of_cohort: number;
}

export interface ExamAnalyticsResponse {
  exam_id: string;
  exam_name: string;
  subject_code: string;
  subject_name: string;
  duration_minutes: number;
  total_marks: number;
  passing_percentage: number;
  score_summary: ScoreSummary;
  pass_fail: PassFailMetrics;
  grade_distribution: GradeBucket[];
  deciles: DecileDistribution[];
  question_metrics: QuestionItemMetric[];
  topic_performance: TopicPerformance[];
  top_performers: CandidateRankItem[];
  at_risk_candidates: CandidateRankItem[];
  generated_at: string;
}

export interface SubjectComparativeMetrics {
  subject_id: string;
  subject_code: string;
  subject_name: string;
  department?: string;
  total_exams: number;
  total_candidates_evaluated: number;
  overall_mean_percentage: number;
  overall_pass_rate: number;
  performance_trend: string;
}

export interface SystemOverviewAnalytics {
  total_users: number;
  total_students: number;
  total_teachers: number;
  total_subjects: number;
  total_questions: number;
  total_exams: number;
  total_attempts_completed: number;
  global_average_score_pct: number;
  global_pass_rate_pct: number;
  active_exams_count: number;
  proctoring_alerts_today: number;
  recent_performance: SubjectComparativeMetrics[];
}
