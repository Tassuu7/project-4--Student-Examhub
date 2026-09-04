"""
ExamHub - Subject Management Endpoints
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from backend.app.subjects.schemas import SubjectCreateRequest, SubjectUpdateRequest, SubjectResponse, AssignTeacherRequest
from backend.app.subjects.service import SubjectService
from backend.app.auth.dependencies import require_admin, require_teacher, require_any_authenticated
from backend.app.auth.schemas import TokenData
from backend.app.core.pagination import PaginationParams, PaginatedResponse
from backend.app.core.exceptions import ExamHubException

router = APIRouter(prefix="/subjects", tags=["Subject Management"])

@router.get("", response_model=PaginatedResponse[SubjectResponse])
def list_subjects(
    search: Optional[str] = None,
    department: Optional[str] = None,
    is_active: Optional[bool] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user: TokenData = Depends(require_any_authenticated)
):
    params = PaginationParams(page=page, page_size=page_size)
    return SubjectService.list_subjects(
        search=search, department=department, is_active=is_active,
        teacher_id=None, params=params
    )

@router.post("", response_model=SubjectResponse)
def create_subject(dto: SubjectCreateRequest, user: TokenData = Depends(require_admin)):
    try:
        return SubjectService.create_subject(dto)
    except ExamHubException as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())

@router.get("/{subject_id}", response_model=SubjectResponse)
def get_subject(subject_id: str, user: TokenData = Depends(require_any_authenticated)):
    try:
        return SubjectService.get_subject(subject_id)
    except ExamHubException as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())

@router.put("/{subject_id}", response_model=SubjectResponse)
def update_subject(subject_id: str, dto: SubjectUpdateRequest, user: TokenData = Depends(require_admin)):
    try:
        return SubjectService.update_subject(subject_id, dto)
    except ExamHubException as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())

@router.post("/{subject_id}/teachers")
def assign_teacher(subject_id: str, dto: AssignTeacherRequest, user: TokenData = Depends(require_admin)):
    try:
        SubjectService.assign_teacher_to_subject(subject_id, dto.teacher_id)
        return {"message": "Teacher assigned to subject successfully."}
    except ExamHubException as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())

@router.delete("/{subject_id}/teachers/{teacher_id}")
def remove_teacher(subject_id: str, teacher_id: str, user: TokenData = Depends(require_admin)):
    try:
        SubjectService.remove_teacher_from_subject(subject_id, teacher_id)
        return {"message": "Teacher removed from subject successfully."}
    except ExamHubException as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())
