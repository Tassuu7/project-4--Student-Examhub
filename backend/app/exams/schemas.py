"""
ExamHub - Exam System Pydantic Schemas & DTOs
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator
from backend.app.core.constants import ExamStatus, AttemptStatus, EvaluationResult, CorrectOption, QuestionDifficulty

class ExamBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    subject_id: str
    description: Optional[str] = None
    duration_minutes: int = Field(..., ge=1, le=480)
    passing_percentage: float = Field(default=40.0, ge=0.0, le=100.0)
    start_date: str
    end_date: str
    instructions: Optional[str] = None

class ExamCreateRequest(ExamBase):
    question_ids: Optional[List[str]] = Field(default_factory=list)
    student_ids: Optional[List[str]] = Field(default_factory=list)

class ExamUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=200)
    subject_id: Optional[str] = None
    description: Optional[str] = None
    duration_minutes: Optional[int] = Field(None, ge=1, le=480)
    passing_percentage: Optional[float] = Field(None, ge=0.0, le=100.0)
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    instructions: Optional[str] = None
    status: Optional[ExamStatus] = None

class ExamStatusUpdateRequest(BaseModel):
    status: ExamStatus

class ExamQuestionItem(BaseModel):
    question_id: str
    marks_allocated: Optional[float] = 1.0

class ExamQuestionAssignmentRequest(BaseModel):
    questions: List[ExamQuestionItem]

class ExamStudentAssignmentRequest(BaseModel):
    student_ids: List[str]

class ExamQuestionPublic(BaseModel):
    id: str
    question_id: str
    order_index: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    marks_allocated: float
    difficulty: str
    topic: Optional[str] = None
    selected_option: Optional[str] = None
    is_marked_for_review: bool = False

class ExamResponse(BaseModel):
    id: str
    name: str
    subject_id: str
    subject_code: str
    subject_name: str
    teacher_id: str
    teacher_name: str
    description: Optional[str] = None
    duration_minutes: int
    total_marks: float
    passing_percentage: float
    start_date: str
    end_date: str
    instructions: Optional[str] = None
    status: ExamStatus
    question_count: int = 0
    assigned_students_count: int = 0
    completed_attempts_count: int = 0
    created_at: str
    updated_at: str

class ExamDetailResponse(ExamResponse):
    questions: List[Dict[str, Any]] = Field(default_factory=list)
    assigned_students: List[Dict[str, Any]] = Field(default_factory=list)

class StudentAnswerSaveRequest(BaseModel):
    question_id: str
    selected_option: Optional[str] = None
    is_marked_for_review: bool = False

    @field_validator("selected_option")
    @classmethod
    def validate_option(cls, v):
        if v is not None and v != "":
            v_upper = v.strip().upper()
            if v_upper not in ["A", "B", "C", "D"]:
                raise ValueError("selected_option must be 'A', 'B', 'C', 'D' or None")
            return v_upper
        return None

class StudentAnswerResponse(BaseModel):
    question_id: str
    selected_option: Optional[str] = None
    is_marked_for_review: bool = False
    saved_at: str

class ExamAttemptStartResponse(BaseModel):
    attempt_id: str
    exam_id: str
    exam_name: str
    subject_code: str
    subject_name: str
    duration_minutes: int
    time_remaining_seconds: int
    start_time: str
    status: AttemptStatus
    questions: List[ExamQuestionPublic]
    instructions: Optional[str] = None

class ExamAttemptSubmitRequest(BaseModel):
    confirm: bool = True

class QuestionReviewItem(BaseModel):
    question_id: str
    order_index: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    selected_option: Optional[str] = None
    correct_answer: str
    is_correct: bool
    marks_obtained: float
    max_marks: float
    explanation: Optional[str] = None
    topic: Optional[str] = None

class ExamResultResponse(BaseModel):
    result_id: str
    attempt_id: str
    exam_id: str
    exam_name: str
    subject_code: str
    subject_name: str
    student_id: str
    student_name: str
    student_roll_number: str
    total_questions: int
    correct_count: int
    wrong_count: int
    unanswered_count: int
    total_marks: float
    obtained_marks: float
    percentage: float
    grade: str
    pass_fail: EvaluationResult
    rank: Optional[int] = None
    total_candidates: Optional[int] = None
    start_time: str
    end_time: Optional[str] = None
    generated_at: str
    review_items: Optional[List[QuestionReviewItem]] = None

class ExamProctoringEventRequest(BaseModel):
    event_type: str = Field(..., description="e.g. tab_switch, window_blur, fullscreen_exit, copy_attempt")
    details: Optional[str] = None

class ExamAutoGenerateRequest(BaseModel):
    subject_id: str
    name: str
    duration_minutes: int = Field(60, ge=5, le=360)
    passing_percentage: float = Field(40.0, ge=0.0, le=100.0)
    start_date: str
    end_date: str
    easy_count: int = Field(0, ge=0)
    medium_count: int = Field(0, ge=0)
    hard_count: int = Field(0, ge=0)
    topic_filter: Optional[str] = None
    instructions: Optional[str] = None
