"""
ExamHub - Authentication FastAPI Dependencies
Enforces Bearer tokens, extracts identity, and validates RBAC
"""

from typing import List, Optional
from fastapi import Header, Depends
from backend.app.core.security import verify_token
from backend.app.core.constants import UserRole
from backend.app.core.exceptions import AuthenticationError, AuthorizationError
from backend.app.auth.schemas import TokenData
from backend.app.auth.service import AuthService, UserProfileDTO

def get_current_user_data(authorization: Optional[str] = Header(None)) -> TokenData:
    if not authorization:
        raise AuthenticationError("Authorization header required")
        
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise AuthenticationError("Invalid Authorization header format. Expected 'Bearer <token>'")
        
    token = parts[1]
    payload = verify_token(token)
    if not payload:
        raise AuthenticationError("Invalid or expired session token")
        
    return TokenData(
        sub=payload["sub"],
        role=UserRole(payload["role"]),
        username=payload["username"],
        email=payload["email"],
        teacher_id=payload.get("teacher_id"),
        student_id=payload.get("student_id")
    )

def require_roles(allowed_roles: List[UserRole]):
    def role_checker(user_data: TokenData = Depends(get_current_user_data)) -> TokenData:
        if user_data.role not in allowed_roles:
            raise AuthorizationError(
                f"Unauthorized role: {user_data.role.value}. Required one of: {[r.value for r in allowed_roles]}"
            )
        return user_data
    return role_checker

# Predefined role dependencies
require_admin = require_roles([UserRole.ADMIN])
require_teacher = require_roles([UserRole.TEACHER, UserRole.ADMIN])
require_student = require_roles([UserRole.STUDENT])
require_any_authenticated = require_roles([UserRole.ADMIN, UserRole.TEACHER, UserRole.STUDENT])

get_current_user = get_current_user_data

def require_role(roles: List[str]):
    user_roles = []
    for r in roles:
        if isinstance(r, UserRole):
            user_roles.append(r)
        elif r == "admin":
            user_roles.append(UserRole.ADMIN)
        elif r == "teacher":
            user_roles.append(UserRole.TEACHER)
        elif r == "student":
            user_roles.append(UserRole.STUDENT)
    return require_roles(user_roles)

