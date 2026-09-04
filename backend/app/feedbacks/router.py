"""
ExamHub - Student Feedback API Router
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.auth.dependencies import (
    require_teacher,
    require_student,
    require_any_authenticated,
    require_admin
)
from backend.app.auth.schemas import TokenData
from backend.app.feedbacks.schemas import FeedbackCreateRequest, FeedbackResponse
from backend.app.feedbacks.repository import FeedbackRepository

router = APIRouter(prefix="/feedbacks", tags=["Feedback"])

@router.post("", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
def submit_feedback(
    req: FeedbackCreateRequest,
    current_user: TokenData = Depends(require_teacher)
):
    teacher_id = current_user.teacher_id
    if not teacher_id:
        # Fallback if admin
        from backend.app.database.connection import get_db_connection
        c = get_db_connection().cursor()
        c.execute("SELECT id FROM teachers LIMIT 1;")
        r = c.fetchone()
        teacher_id = r[0] if r else "t_default"

    fb = FeedbackRepository.create_or_update(
        exam_id=req.exam_id,
        student_id=req.student_id,
        teacher_id=teacher_id,
        feedback_text=req.feedback_text,
        rating=req.rating or 5,
        attempt_id=req.attempt_id
    )
    return fb

@router.get("/student/{student_id}", response_model=List[FeedbackResponse])
def get_student_feedbacks(
    student_id: str,
    current_user: TokenData = Depends(require_any_authenticated)
):
    return FeedbackRepository.list_by_student(student_id)

@router.get("/exam/{exam_id}", response_model=List[FeedbackResponse])
def get_exam_feedbacks(
    exam_id: str,
    current_user: TokenData = Depends(require_any_authenticated)
):
    return FeedbackRepository.list_by_exam(exam_id)

@router.get("", response_model=List[FeedbackResponse])
def list_all_feedbacks(
    current_user: TokenData = Depends(require_any_authenticated)
):
    return FeedbackRepository.list_all()
