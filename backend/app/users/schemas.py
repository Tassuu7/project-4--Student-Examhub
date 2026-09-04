"""
ExamHub - User Schemas and DTOs
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from backend.app.core.constants import UserRole

class UserCreateRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)
    full_name: str = Field(..., min_length=2, max_length=100)
    role: UserRole
    # Student specific
    student_id_code: Optional[str] = None
    grade_level: Optional[str] = None
    department: Optional[str] = None
    phone: Optional[str] = None
    guardian_contact: Optional[str] = None
    # Teacher specific
    teacher_id_code: Optional[str] = None
    qualification: Optional[str] = None
    specialization: Optional[str] = None

class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    department: Optional[str] = None
    phone: Optional[str] = None
    grade_level: Optional[str] = None
    qualification: Optional[str] = None
    specialization: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    full_name: str
    role: UserRole
    is_active: bool
    created_at: str
    updated_at: str
    # Polymorphic metadata
    code: Optional[str] = None
    department: Optional[str] = None
    phone: Optional[str] = None
    grade_level: Optional[str] = None
    qualification: Optional[str] = None
    specialization: Optional[str] = None
