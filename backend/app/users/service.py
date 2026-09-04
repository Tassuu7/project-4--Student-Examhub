"""
ExamHub - User Business Service
"""

from typing import Optional, List, Dict, Any
from backend.app.users.repository import UserRepository
from backend.app.users.schemas import UserCreateRequest, UserUpdateRequest, UserResponse
from backend.app.core.constants import UserRole
from backend.app.core.exceptions import ValidationError, ResourceNotFoundError
from backend.app.core.pagination import PaginationParams, PaginatedResponse

class UserService:
    @staticmethod
    def create_user(dto: UserCreateRequest) -> UserResponse:
        # Check duplicate username
        if UserRepository.get_by_username(dto.username):
            raise ValidationError(f"Username '{dto.username}' is already taken.")
        if UserRepository.get_by_email(dto.email):
            raise ValidationError(f"Email '{dto.email}' is already registered.")
            
        user_id = UserRepository.create_user(dto.model_dump())
        raw = UserRepository.get_by_id(user_id)
        return UserResponse(
            id=raw["id"],
            username=raw["username"],
            email=raw["email"],
            full_name=raw["full_name"],
            role=UserRole(raw["role"]),
            is_active=bool(raw["is_active"]),
            created_at=raw["created_at"],
            updated_at=raw["updated_at"],
            code=raw.get("student_id_code") or raw.get("teacher_id_code"),
            department=raw.get("student_dept") or raw.get("teacher_dept"),
            phone=raw.get("student_phone"),
            grade_level=raw.get("grade_level"),
            qualification=raw.get("qualification"),
            specialization=raw.get("specialization")
        )

    @staticmethod
    def update_user(user_id: str, dto: UserUpdateRequest) -> UserResponse:
        existing = UserRepository.get_by_id(user_id)
        if not existing:
            raise ResourceNotFoundError("User", user_id)
            
        if dto.email and dto.email.lower() != existing["email"].lower():
            dup = UserRepository.get_by_email(dto.email)
            if dup and dup["id"] != user_id:
                raise ValidationError(f"Email '{dto.email}' is already registered to another user.")
                
        UserRepository.update_user(user_id, dto.model_dump(exclude_unset=True))
        raw = UserRepository.get_by_id(user_id)
        return UserResponse(
            id=raw["id"],
            username=raw["username"],
            email=raw["email"],
            full_name=raw["full_name"],
            role=UserRole(raw["role"]),
            is_active=bool(raw["is_active"]),
            created_at=raw["created_at"],
            updated_at=raw["updated_at"],
            code=raw.get("student_id_code") or raw.get("teacher_id_code"),
            department=raw.get("student_dept") or raw.get("teacher_dept"),
            phone=raw.get("student_phone"),
            grade_level=raw.get("grade_level"),
            qualification=raw.get("qualification"),
            specialization=raw.get("specialization")
        )

    @staticmethod
    def get_user_by_id(user_id: str) -> UserResponse:
        raw = UserRepository.get_by_id(user_id)
        if not raw:
            raise ResourceNotFoundError("User", user_id)
        return UserResponse(
            id=raw["id"],
            username=raw["username"],
            email=raw["email"],
            full_name=raw["full_name"],
            role=UserRole(raw["role"]),
            is_active=bool(raw["is_active"]),
            created_at=raw["created_at"],
            updated_at=raw["updated_at"],
            code=raw.get("student_id_code") or raw.get("teacher_id_code"),
            department=raw.get("student_dept") or raw.get("teacher_dept"),
            phone=raw.get("student_phone"),
            grade_level=raw.get("grade_level"),
            qualification=raw.get("qualification"),
            specialization=raw.get("specialization")
        )

    @staticmethod
    def list_users(role: Optional[UserRole], search: Optional[str], is_active: Optional[bool], params: PaginationParams) -> PaginatedResponse[UserResponse]:
        items_raw, total = UserRepository.list_users(role=role, search=search, is_active=is_active, offset=params.offset, limit=params.limit)
        items = [
            UserResponse(
                id=r["id"],
                username=r["username"],
                email=r["email"],
                full_name=r["full_name"],
                role=UserRole(r["role"]),
                is_active=bool(r["is_active"]),
                created_at=r["created_at"],
                updated_at=r["updated_at"],
                code=r.get("code"),
                department=r.get("department"),
                phone=r.get("phone"),
                grade_level=r.get("grade_level"),
                qualification=r.get("qualification"),
                specialization=r.get("specialization")
            )
            for r in items_raw
        ]
        return PaginatedResponse.create(items, total, params)

    @staticmethod
    def toggle_user_active(user_id: str, is_active: bool):
        existing = UserRepository.get_by_id(user_id)
        if not existing:
            raise ResourceNotFoundError("User", user_id)
        UserRepository.toggle_active(user_id, is_active)
