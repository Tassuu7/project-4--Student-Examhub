"""
ExamHub - Role-Based Access Control (RBAC) Enforcement
"""

from typing import List, Set
from backend.app.core.constants import UserRole
from backend.app.core.exceptions import AuthorizationError

ROLE_PERMISSIONS: dict[UserRole, Set[str]] = {
    UserRole.ADMIN: {
        "admin:all",
        "users:create", "users:read", "users:update", "users:delete",
        "students:manage", "teachers:manage", "subjects:manage",
        "exams:read_all", "exams:activate", "exams:deactivate",
        "questions:read_all", "results:read_all", "results:export",
        "reports:generate", "audit:read"
    },
    UserRole.TEACHER: {
        "subjects:read_assigned",
        "questions:create", "questions:read", "questions:update", "questions:delete",
        "exams:create", "exams:read_own", "exams:update_own", "exams:delete_own", "exams:schedule",
        "attempts:read_assigned", "results:read_assigned", "analytics:read_assigned",
        "reports:read_assigned"
    },
    UserRole.STUDENT: {
        "exams:read_assigned", "exams:attempt",
        "answers:submit", "results:read_own", "performance:read_own",
        "notifications:read_own", "profile:read_own"
    }
}

def verify_role_access(user_role: str, allowed_roles: List[UserRole]):
    """Strictly verify user role matches the required permission set."""
    try:
        current_role = UserRole(user_role)
    except ValueError:
        raise AuthorizationError("Unknown user role")
        
    if current_role not in allowed_roles:
        raise AuthorizationError(
            f"Role '{user_role}' is not authorized to access this resource. Allowed: {[r.value for r in allowed_roles]}"
        )

def verify_student_self_access(current_user_id: str, student_user_id: str, user_role: str):
    """Ensure student can only inspect their own records; teachers and admins have broader access."""
    if user_role == UserRole.STUDENT.value and current_user_id != student_user_id:
        raise AuthorizationError("Access denied: You can only view your own records.")

from backend.app.auth.dependencies import require_role
