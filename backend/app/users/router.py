"""
ExamHub - User Management Endpoints (Admin Controlled)
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from backend.app.users.schemas import UserCreateRequest, UserUpdateRequest, UserResponse
from backend.app.users.service import UserService
from backend.app.auth.dependencies import require_admin, require_any_authenticated, require_teacher
from backend.app.auth.schemas import TokenData
from backend.app.core.constants import UserRole
from backend.app.core.pagination import PaginationParams, PaginatedResponse
from backend.app.core.exceptions import ExamHubException
from backend.app.database.connection import get_db_connection

router = APIRouter(prefix="/users", tags=["User Management"])

@router.get("/students")
def list_students(
    user: TokenData = Depends(require_teacher)
):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """SELECT s.id as student_id, s.student_id_code, s.grade_level, s.department,
                  u.id as user_id, u.full_name, u.email, u.username
           FROM students s
           JOIN users u ON s.user_id = u.id
           WHERE u.is_active = 1
           ORDER BY s.student_id_code ASC;"""
    )
    rows = c.fetchall()
    items = [
        {
            "id": r["student_id"],
            "student_id": r["student_id"],
            "student_id_code": r["student_id_code"],
            "full_name": r["full_name"],
            "email": r["email"],
            "department": r["department"],
            "grade_level": r["grade_level"]
        }
        for r in rows
    ]
    return {"items": items, "total": len(items)}

@router.get("", response_model=PaginatedResponse[UserResponse])
def list_users(
    role: Optional[UserRole] = None,
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    user: TokenData = Depends(require_admin)
):
    params = PaginationParams(page=page, page_size=page_size)
    return UserService.list_users(role=role, search=search, is_active=is_active, params=params)

@router.post("", response_model=UserResponse)
def create_user(dto: UserCreateRequest, user: TokenData = Depends(require_admin)):
    try:
        return UserService.create_user(dto)
    except ExamHubException as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, user: TokenData = Depends(require_any_authenticated)):
    try:
        return UserService.get_user_by_id(user_id)
    except ExamHubException as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: str, dto: UserUpdateRequest, user: TokenData = Depends(require_admin)):
    try:
        return UserService.update_user(user_id, dto)
    except ExamHubException as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())

@router.patch("/{user_id}/status")
def toggle_status(user_id: str, is_active: bool = Query(...), user: TokenData = Depends(require_admin)):
    try:
        UserService.toggle_user_active(user_id, is_active)
        return {"message": f"User status updated to {'active' if is_active else 'inactive'}."}
    except ExamHubException as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())
