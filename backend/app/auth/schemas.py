"""
ExamHub - Authentication Schemas & DTOs
"""

from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from backend.app.core.constants import UserRole

class LoginRequest(BaseModel):
    username_or_email: str = Field(..., description="Username or email address", min_length=3)
    password: str = Field(..., description="Account password", min_length=4)

class UserProfileDTO(BaseModel):
    id: str
    username: str
    email: str
    full_name: str
    role: UserRole
    is_active: bool
    student_id: Optional[str] = None
    student_code: Optional[str] = None
    teacher_id: Optional[str] = None
    teacher_code: Optional[str] = None
    department: Optional[str] = None
    created_at: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserProfileDTO

class PasswordChangeRequest(BaseModel):
    current_password: str = Field(..., min_length=4)
    new_password: str = Field(..., min_length=6)

class TokenData(BaseModel):
    sub: str
    role: UserRole
    username: str
    email: str
    teacher_id: Optional[str] = None
    student_id: Optional[str] = None
