"""
ExamHub - Authentication Business Service
Handles user verification, token issuing, role resolution, and password management
"""

import sqlite3
from typing import Optional, Tuple, Dict, Any
from backend.app.database.connection import get_db_connection, dict_from_row, transaction
from backend.app.core.security import verify_password, hash_password, generate_token
from backend.app.core.constants import UserRole
from backend.app.core.exceptions import AuthenticationError, ResourceNotFoundError, ValidationError
from backend.app.auth.schemas import UserProfileDTO, TokenResponse

class AuthService:
    @staticmethod
    def authenticate_user(username_or_email: str, password: str) -> Tuple[UserProfileDTO, str]:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT id, username, email, password_hash, full_name, role, is_active, created_at
               FROM users
               WHERE username = ? OR email = ?;""",
            (username_or_email.strip(), username_or_email.strip().lower())
        )
        row = cursor.fetchone()
        if not row:
            raise AuthenticationError("Invalid username or password.")
            
        user = dict_from_row(row)
        if not user["is_active"]:
            raise AuthenticationError("Account has been deactivated. Please contact an administrator.")
            
        if not verify_password(password, user["password_hash"]):
            raise AuthenticationError("Invalid username or password.")
            
        # Enrich with role-specific identifiers
        student_id, student_code, teacher_id, teacher_code, dept = None, None, None, None, None
        
        if user["role"] == UserRole.STUDENT.value:
            cursor.execute("SELECT id, student_id_code, department FROM students WHERE user_id = ?;", (user["id"],))
            s_row = cursor.fetchone()
            if s_row:
                student_id = s_row["id"]
                student_code = s_row["student_id_code"]
                dept = s_row["department"]
        elif user["role"] == UserRole.TEACHER.value:
            cursor.execute("SELECT id, teacher_id_code, department FROM teachers WHERE user_id = ?;", (user["id"],))
            t_row = cursor.fetchone()
            if t_row:
                teacher_id = t_row["id"]
                teacher_code = t_row["teacher_id_code"]
                dept = t_row["department"]

        profile = UserProfileDTO(
            id=user["id"],
            username=user["username"],
            email=user["email"],
            full_name=user["full_name"],
            role=UserRole(user["role"]),
            is_active=bool(user["is_active"]),
            student_id=student_id,
            student_code=student_code,
            teacher_id=teacher_id,
            teacher_code=teacher_code,
            department=dept,
            created_at=user["created_at"]
        )

        token_payload = {
            "sub": user["id"],
            "role": user["role"],
            "username": user["username"],
            "email": user["email"],
            "student_id": student_id,
            "teacher_id": teacher_id
        }
        token = generate_token(token_payload)
        return profile, token

    @staticmethod
    def get_user_profile(user_id: str) -> UserProfileDTO:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, full_name, role, is_active, created_at FROM users WHERE id = ?;", (user_id,))
        row = cursor.fetchone()
        if not row:
            raise ResourceNotFoundError("User", user_id)
            
        user = dict_from_row(row)
        student_id, student_code, teacher_id, teacher_code, dept = None, None, None, None, None
        
        if user["role"] == UserRole.STUDENT.value:
            cursor.execute("SELECT id, student_id_code, department FROM students WHERE user_id = ?;", (user["id"],))
            s_row = cursor.fetchone()
            if s_row:
                student_id = s_row["id"]
                student_code = s_row["student_id_code"]
                dept = s_row["department"]
        elif user["role"] == UserRole.TEACHER.value:
            cursor.execute("SELECT id, teacher_id_code, department FROM teachers WHERE user_id = ?;", (user["id"],))
            t_row = cursor.fetchone()
            if t_row:
                teacher_id = t_row["id"]
                teacher_code = t_row["teacher_id_code"]
                dept = t_row["department"]

        return UserProfileDTO(
            id=user["id"],
            username=user["username"],
            email=user["email"],
            full_name=user["full_name"],
            role=UserRole(user["role"]),
            is_active=bool(user["is_active"]),
            student_id=student_id,
            student_code=student_code,
            teacher_id=teacher_id,
            teacher_code=teacher_code,
            department=dept,
            created_at=user["created_at"]
        )

    @staticmethod
    def change_password(user_id: str, current_pass: str, new_pass: str):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE id = ?;", (user_id,))
        row = cursor.fetchone()
        if not row:
            raise ResourceNotFoundError("User", user_id)
            
        if not verify_password(current_pass, row["password_hash"]):
            raise ValidationError("Current password does not match.")
            
        new_hash = hash_password(new_pass)
        with transaction():
            cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?;", (new_hash, user_id))
