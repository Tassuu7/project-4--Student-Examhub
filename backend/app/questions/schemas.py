"""
ExamHub - Question Bank Schemas & DTOs
"""

from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from backend.app.core.constants import QuestionDifficulty, CorrectOption

class QuestionCreateRequest(BaseModel):
    subject_id: str = Field(..., description="Subject identifier")
    question_text: str = Field(..., min_length=5, description="Full question statement")
    option_a: str = Field(..., min_length=1, description="Option A")
    option_b: str = Field(..., min_length=1, description="Option B")
    option_c: str = Field(..., min_length=1, description="Option C")
    option_d: str = Field(..., min_length=1, description="Option D")
    correct_answer: CorrectOption = Field(..., description="Correct option: A, B, C, or D")
    marks: float = Field(1.0, gt=0, le=100, description="Score marks allocated for question")
    difficulty: QuestionDifficulty = Field(QuestionDifficulty.MEDIUM, description="Difficulty level")
    topic: Optional[str] = Field(None, max_length=100, description="Specific topic or sub-concept")
    explanation: Optional[str] = Field(None, description="Detailed explanation of the correct answer")

    @field_validator("correct_answer", mode="before")
    @classmethod
    def normalize_correct_answer(cls, v):
        if isinstance(v, str):
            return v.strip().upper()
        return v

class QuestionUpdateRequest(BaseModel):
    subject_id: Optional[str] = None
    question_text: Optional[str] = Field(None, min_length=5)
    option_a: Optional[str] = Field(None, min_length=1)
    option_b: Optional[str] = Field(None, min_length=1)
    option_c: Optional[str] = Field(None, min_length=1)
    option_d: Optional[str] = Field(None, min_length=1)
    correct_answer: Optional[CorrectOption] = None
    marks: Optional[float] = Field(None, gt=0, le=100)
    difficulty: Optional[QuestionDifficulty] = None
    topic: Optional[str] = Field(None, max_length=100)
    explanation: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator("correct_answer", mode="before")
    @classmethod
    def normalize_correct_answer(cls, v):
        if isinstance(v, str):
            return v.strip().upper()
        return v

class QuestionResponse(BaseModel):
    id: str
    subject_id: str
    subject_code: str
    subject_name: str
    teacher_id: Optional[str] = None
    teacher_name: Optional[str] = None
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str
    marks: float
    difficulty: str
    topic: Optional[str] = None
    explanation: Optional[str] = None
    is_active: bool
    used_in_exam_count: int = 0
    created_at: str
    updated_at: str

class BulkImportSummary(BaseModel):
    total_processed: int
    imported_count: int
    failed_count: int
    errors: List[str] = []
