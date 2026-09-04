"""
ExamHub - Student Feedback Pydantic Schemas
"""

from typing import Optional
from pydantic import BaseModel, Field

class FeedbackCreateRequest(BaseModel):
    exam_id: str
    student_id: str
    attempt_id: Optional[str] = None
    feedback_text: str = Field(..., min_length=2, max_length=2000)
    rating: Optional[int] = Field(5, ge=1, le=5)

class FeedbackUpdateRequest(BaseModel):
    feedback_text: str = Field(..., min_length=2, max_length=2000)
    rating: Optional[int] = Field(5, ge=1, le=5)

class FeedbackResponse(BaseModel):
    id: str
    exam_id: str
    exam_name: str
    subject_code: str
    subject_name: str
    student_id: str
    student_name: str
    student_roll_number: str
    teacher_id: str
    teacher_name: str
    attempt_id: Optional[str] = None
    feedback_text: str
    rating: int
    created_at: str
    updated_at: str
