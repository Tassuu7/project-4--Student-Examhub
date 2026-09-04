"""
ExamHub - Psychometric and Examination Analytics Schemas
Defines request and response data contracts for exam psychometrics,
item response theory (IRT), grade distributions, and cohort comparisons.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ScoreSummary(BaseModel):
    total_candidates: int
    evaluated_candidates: int
    mean_score: float
    median_score: float
    mode_score: Optional[float] = None
    standard_deviation: float
    variance: float
    minimum_score: float
    maximum_score: float
    range_score: float
    q1_score: float
    q3_score: float
    iqr_score: float
    skewness: float
    kurtosis: float

class GradeBucket(BaseModel):
    grade: str
    count: int
    percentage: float
    min_score: float
    max_score: float
    color_code: str

class PassFailMetrics(BaseModel):
    total_appeared: int
    passed_count: int
    failed_count: int
    passing_percentage: float
    pass_rate: float
    fail_rate: float
    threshold_marks: float

class QuestionItemMetric(BaseModel):
    question_id: str
    order_index: int
    question_text: str
    difficulty_assigned: str
    topic: Optional[str] = None
    marks_allocated: float
    total_attempts: int
    correct_attempts: int
    wrong_attempts: int
    unanswered_attempts: int
    facility_index: float  # Item Difficulty Index (P-value: 0.0 to 1.0)
    discrimination_index: float  # Item Discrimination Index (D-value: -1.0 to 1.0)
    point_biserial: float  # Point-biserial correlation coefficient
    discrimination_status: str  # Excellent, Good, Marginal, Poor, Defective
    option_a_selection_rate: float
    option_b_selection_rate: float
    option_c_selection_rate: float
    option_d_selection_rate: float
    average_time_seconds: Optional[float] = None

class TopicPerformance(BaseModel):
    topic: str
    question_count: int
    total_marks: float
    average_accuracy_percentage: float
    mastery_level: str  # Mastered, Proficient, Developing, Novice
    weak_student_count: int
    strong_student_count: int

class CandidateRankItem(BaseModel):
    rank: int
    student_id: str
    user_id: str
    full_name: str
    roll_number: str
    obtained_marks: float
    total_marks: float
    percentage: float
    grade: str
    pass_fail: str
    percentile: float
    completion_time_seconds: int
    time_taken_formatted: str
    submitted_at: str

class DecileDistribution(BaseModel):
    decile: str  # e.g., "0-10%", "10-20%"
    lower_bound: float
    upper_bound: float
    student_count: int
    percentage_of_cohort: float

class ExamAnalyticsResponse(BaseModel):
    exam_id: str
    exam_name: str
    subject_code: str
    subject_name: str
    duration_minutes: int
    total_marks: float
    passing_percentage: float
    score_summary: ScoreSummary
    pass_fail: PassFailMetrics
    grade_distribution: List[GradeBucket]
    deciles: List[DecileDistribution]
    question_metrics: List[QuestionItemMetric]
    topic_performance: List[TopicPerformance]
    top_performers: List[CandidateRankItem]
    at_risk_candidates: List[CandidateRankItem]
    generated_at: str

class SubjectComparativeMetrics(BaseModel):
    subject_id: str
    subject_code: str
    subject_name: str
    department: Optional[str] = None
    total_exams: int
    total_candidates_evaluated: int
    overall_mean_percentage: float
    overall_pass_rate: float
    highest_scoring_exam: Optional[str] = None
    lowest_scoring_exam: Optional[str] = None
    performance_trend: str  # Improving, Stable, Declining

class SystemOverviewAnalytics(BaseModel):
    total_users: int
    total_students: int
    total_teachers: int
    total_subjects: int
    total_questions: int
    total_exams: int
    total_attempts_completed: int
    global_average_score_pct: float
    global_pass_rate_pct: float
    active_exams_count: int
    proctoring_alerts_today: int
    recent_performance: List[SubjectComparativeMetrics]

class CohortComparisonRequest(BaseModel):
    cohort_a_exam_id: str
    cohort_b_exam_id: str
    metrics: Optional[List[str]] = Field(default_factory=lambda: ["mean", "pass_rate", "discrimination"])

class CohortComparisonResult(BaseModel):
    cohort_a_name: str
    cohort_b_name: str
    cohort_a_size: int
    cohort_b_size: int
    cohort_a_mean: float
    cohort_b_mean: float
    mean_difference: float
    effect_size_cohens_d: float
    t_statistic: float
    p_value: float
    is_statistically_significant: bool
    summary: str
