"""
ExamHub - Exam Management & Execution REST API Router
"""

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, Query, status
from backend.app.auth.dependencies import (
    require_teacher,
    require_student,
    require_any_authenticated,
    require_admin
)
from backend.app.auth.schemas import TokenData
from backend.app.exams.service import ExamService
from backend.app.exams.repository import ExamRepository
from backend.app.exams.proctoring import ProctoringService
from backend.app.exams.schemas import (
    ExamCreateRequest,
    ExamUpdateRequest,
    ExamStatusUpdateRequest,
    ExamQuestionAssignmentRequest,
    ExamStudentAssignmentRequest,
    ExamAutoGenerateRequest,
    StudentAnswerSaveRequest,
    ExamAttemptStartResponse,
    ExamResultResponse,
    ExamProctoringEventRequest,
    ExamDetailResponse
)

router = APIRouter(prefix="/exams", tags=["Exams"])

@router.post("", status_code=status.HTTP_201_CREATED)
def create_exam(
    req: ExamCreateRequest,
    current_user: TokenData = Depends(require_teacher)
):
    exam_id = ExamService.create_exam(req, current_user)
    return {"message": "Exam created successfully", "exam_id": exam_id}

@router.post("/auto-generate", status_code=status.HTTP_201_CREATED)
def auto_generate_exam(
    req: ExamAutoGenerateRequest,
    current_user: TokenData = Depends(require_teacher)
):
    exam_id = ExamService.auto_generate_exam(req, current_user)
    return {"message": "Exam auto-generated successfully", "exam_id": exam_id}

@router.get("")
def list_exams(
    subject_id: Optional[str] = Query(None),
    teacher_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: TokenData = Depends(require_any_authenticated)
):
    offset = (page - 1) * limit
    exams, total = ExamRepository.list_exams(
        subject_id=subject_id,
        teacher_id=teacher_id,
        status=status,
        search=search,
        offset=offset,
        limit=limit
    )
    return {
        "items": exams,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit if total > 0 else 1
    }

@router.get("/student/portal")
def get_student_assigned_exams(
    current_user: TokenData = Depends(require_student)
):
    student_id = current_user.student_id
    exams = ExamRepository.get_student_assigned_exams(student_id)
    return {"items": exams, "total": len(exams)}

@router.get("/{exam_id}")
def get_exam_details(
    exam_id: str,
    current_user: TokenData = Depends(require_any_authenticated)
):
    return ExamService.get_exam_details(exam_id)

@router.put("/{exam_id}")
def update_exam(
    exam_id: str,
    req: ExamUpdateRequest,
    current_user: TokenData = Depends(require_teacher)
):
    updated = ExamService.update_exam(exam_id, req, current_user)
    return {"message": "Exam updated successfully", "exam": updated}

@router.delete("/{exam_id}")
def delete_exam(
    exam_id: str,
    current_user: TokenData = Depends(require_teacher)
):
    ExamService.delete_exam(exam_id, current_user)
    return {"message": "Exam deleted successfully"}

@router.put("/{exam_id}/status")
def update_exam_status(
    exam_id: str,
    req: ExamStatusUpdateRequest,
    current_user: TokenData = Depends(require_teacher)
):
    ExamRepository.update_exam(exam_id, {"status": req.status.value})
    return {"message": f"Exam status updated to {req.status.value}"}

@router.post("/{exam_id}/questions")
def assign_questions_to_exam(
    exam_id: str,
    req: ExamQuestionAssignmentRequest,
    current_user: TokenData = Depends(require_teacher)
):
    return ExamService.assign_questions(exam_id, req)

@router.post("/{exam_id}/students")
def assign_students_to_exam(
    exam_id: str,
    req: ExamStudentAssignmentRequest,
    current_user: TokenData = Depends(require_teacher)
):
    return ExamService.assign_students(exam_id, req)

# Attempt Endpoints
@router.post("/{exam_id}/attempt/start", response_model=ExamAttemptStartResponse)
def start_exam_attempt(
    exam_id: str,
    current_user: TokenData = Depends(require_student)
):
    return ExamService.start_exam_attempt(exam_id, current_user)

@router.post("/attempt/{attempt_id}/answer")
def save_student_answer(
    attempt_id: str,
    req: StudentAnswerSaveRequest,
    current_user: TokenData = Depends(require_student)
):
    return ExamService.save_answer(attempt_id, req, current_user)

@router.post("/attempt/{attempt_id}/time")
def update_time_remaining(
    attempt_id: str,
    payload: Dict[str, int],
    current_user: TokenData = Depends(require_student)
):
    seconds = payload.get("time_remaining_seconds", 0)
    ExamService.update_time_remaining(attempt_id, seconds, current_user)
    return {"status": "ok"}

@router.post("/attempt/{attempt_id}/submit", response_model=ExamResultResponse)
def submit_exam_attempt(
    attempt_id: str,
    current_user: TokenData = Depends(require_student)
):
    return ExamService.submit_exam_attempt(attempt_id, auto_submitted=False)

@router.post("/attempt/{attempt_id}/auto-submit", response_model=ExamResultResponse)
def auto_submit_exam_attempt(
    attempt_id: str,
    current_user: TokenData = Depends(require_student)
):
    return ExamService.submit_exam_attempt(attempt_id, auto_submitted=True)

@router.post("/attempt/{attempt_id}/proctoring")
def log_proctoring_event(
    attempt_id: str,
    req: ExamProctoringEventRequest,
    current_user: TokenData = Depends(require_student)
):
    ProctoringService.record_event(attempt_id, req.event_type, req.details)
    return {"status": "recorded"}

@router.get("/attempt/{attempt_id}/result", response_model=ExamResultResponse)
def get_attempt_result(
    attempt_id: str,
    current_user: TokenData = Depends(require_any_authenticated)
):
    return ExamService.get_result(attempt_id, current_user)

@router.get("/{exam_id}/results")
def list_exam_results(
    exam_id: str,
    current_user: TokenData = Depends(require_teacher)
):
    results = ExamRepository.list_exam_results(exam_id)
    return {"items": results, "total": len(results)}

@router.get("/attempt/{attempt_id}/integrity")
def get_attempt_integrity(
    attempt_id: str,
    current_user: TokenData = Depends(require_teacher)
):
    return ProctoringService.get_integrity_summary(attempt_id)
