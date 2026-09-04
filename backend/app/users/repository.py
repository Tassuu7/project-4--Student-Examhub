"""
ExamHub - User Data Access Repository
"""

import uuid
import datetime
from typing import Optional, List, Dict, Any, Tuple
from backend.app.database.connection import get_db_connection, dict_from_row, list_from_rows, transaction
from backend.app.core.constants import UserRole
from backend.app.core.security import hash_password

class UserRepository:
    @staticmethod
    def get_by_id(user_id: str) -> Optional[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT u.id, u.username, u.email, u.full_name, u.role, u.is_active, u.created_at, u.updated_at,
                      s.student_id_code, s.grade_level, s.department as student_dept, s.phone as student_phone,
                      t.teacher_id_code, t.department as teacher_dept, t.qualification, t.specialization
               FROM users u
               LEFT JOIN students s ON u.id = s.user_id
               LEFT JOIN teachers t ON u.id = t.user_id
               WHERE u.id = ?;""",
            (user_id,)
        )
        return dict_from_row(cursor.fetchone())

    @staticmethod
    def get_by_username(username: str) -> Optional[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?;", (username.strip(),))
        return dict_from_row(cursor.fetchone())

    @staticmethod
    def get_by_email(email: str) -> Optional[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?;", (email.strip().lower(),))
        return dict_from_row(cursor.fetchone())

    @staticmethod
    def list_users(role: Optional[UserRole] = None, search: Optional[str] = None, is_active: Optional[bool] = None,
                   offset: int = 0, limit: int = 10) -> Tuple[List[Dict[str, Any]], int]:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT u.id, u.username, u.email, u.full_name, u.role, u.is_active, u.created_at, u.updated_at,
                   COALESCE(s.student_id_code, t.teacher_id_code) as code,
                   COALESCE(s.department, t.department) as department,
                   s.phone, s.grade_level, t.qualification, t.specialization
            FROM users u
            LEFT JOIN students s ON u.id = s.user_id
            LEFT JOIN teachers t ON u.id = t.user_id
            WHERE 1=1
        """
        count_query = "SELECT COUNT(*) FROM users u LEFT JOIN students s ON u.id = s.user_id LEFT JOIN teachers t ON u.id = t.user_id WHERE 1=1"
        params = []
        
        if role:
            query += " AND u.role = ?"
            count_query += " AND u.role = ?"
            params.append(role.value)
            
        if is_active is not None:
            query += " AND u.is_active = ?"
            count_query += " AND u.is_active = ?"
            params.append(1 if is_active else 0)
            
        if search:
            s_param = f"%{search.strip().lower()}%"
            filter_str = " AND (LOWER(u.username) LIKE ? OR LOWER(u.email) LIKE ? OR LOWER(u.full_name) LIKE ? OR LOWER(s.student_id_code) LIKE ? OR LOWER(t.teacher_id_code) LIKE ?)"
            query += filter_str
            count_query += filter_str
            params.extend([s_param, s_param, s_param, s_param, s_param])
            
        cursor.execute(count_query, params)
        total = cursor.fetchone()[0]
        
        query += " ORDER BY u.created_at DESC LIMIT ? OFFSET ?;"
        cursor.execute(query, params + [limit, offset])
        items = list_from_rows(cursor.fetchall())
        
        return items, total

    @staticmethod
    def create_user(data: Dict[str, Any]) -> str:
        user_id = str(uuid.uuid4())
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        pwd_hash = hash_password(data["password"])
        
        with transaction():
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO users (id, username, email, password_hash, full_name, role, is_active, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?);""",
                (user_id, data["username"].strip(), data["email"].strip().lower(), pwd_hash, data["full_name"].strip(), data["role"].value, now, now)
            )
            
            if data["role"] == UserRole.STUDENT:
                student_id = str(uuid.uuid4())
                cursor.execute(
                    """INSERT INTO students (id, user_id, student_id_code, grade_level, department, phone, guardian_contact, enrolled_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?);""",
                    (student_id, user_id, data.get("student_id_code") or f"STU{user_id[:6].upper()}",
                     data.get("grade_level"), data.get("department"), data.get("phone"), data.get("guardian_contact"), now)
                )
            elif data["role"] == UserRole.TEACHER:
                teacher_id = str(uuid.uuid4())
                cursor.execute(
                    """INSERT INTO teachers (id, user_id, teacher_id_code, department, qualification, specialization, hired_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?);""",
                    (teacher_id, user_id, data.get("teacher_id_code") or f"TCH{user_id[:6].upper()}",
                     data.get("department"), data.get("qualification"), data.get("specialization"), now)
                )
                
        return user_id

    @staticmethod
    def update_user(user_id: str, data: Dict[str, Any]):
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        conn = get_db_connection()
        cursor = conn.cursor()
        
        with transaction():
            fields = []
            params = []
            if "full_name" in data and data["full_name"] is not None:
                fields.append("full_name = ?")
                params.append(data["full_name"].strip())
            if "email" in data and data["email"] is not None:
                fields.append("email = ?")
                params.append(data["email"].strip().lower())
            if "is_active" in data and data["is_active"] is not None:
                fields.append("is_active = ?")
                params.append(1 if data["is_active"] else 0)
                
            if fields:
                fields.append("updated_at = ?")
                params.append(now)
                params.append(user_id)
                cursor.execute(f"UPDATE users SET {', '.join(fields)} WHERE id = ?;", params)
                
            # Update student/teacher extra fields
            cursor.execute("SELECT role FROM users WHERE id = ?;", (user_id,))
            r_row = cursor.fetchone()
            if r_row and r_row["role"] == UserRole.STUDENT.value:
                s_fields, s_params = [], []
                if "department" in data and data["department"] is not None:
                    s_fields.append("department = ?"); s_params.append(data["department"])
                if "phone" in data and data["phone"] is not None:
                    s_fields.append("phone = ?"); s_params.append(data["phone"])
                if "grade_level" in data and data["grade_level"] is not None:
                    s_fields.append("grade_level = ?"); s_params.append(data["grade_level"])
                if s_fields:
                    s_params.append(user_id)
                    cursor.execute(f"UPDATE students SET {', '.join(s_fields)} WHERE user_id = ?;", s_params)
            elif r_row and r_row["role"] == UserRole.TEACHER.value:
                t_fields, t_params = [], []
                if "department" in data and data["department"] is not None:
                    t_fields.append("department = ?"); t_params.append(data["department"])
                if "qualification" in data and data["qualification"] is not None:
                    t_fields.append("qualification = ?"); t_params.append(data["qualification"])
                if "specialization" in data and data["specialization"] is not None:
                    t_fields.append("specialization = ?"); t_params.append(data["specialization"])
                if t_fields:
                    t_params.append(user_id)
                    cursor.execute(f"UPDATE teachers SET {', '.join(t_fields)} WHERE user_id = ?;", t_params)

    @staticmethod
    def toggle_active(user_id: str, is_active: bool):
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with transaction():
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET is_active = ?, updated_at = ? WHERE id = ?;", (1 if is_active else 0, now, user_id))
