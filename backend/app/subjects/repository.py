"""
ExamHub - Subject Data Access Repository
"""

import uuid
import datetime
from typing import Optional, List, Dict, Any, Tuple
from backend.app.database.connection import get_db_connection, dict_from_row, list_from_rows, transaction

class SubjectRepository:
    @staticmethod
    def get_by_id(subject_id: str) -> Optional[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT s.id, s.code, s.name, s.description, s.department, s.is_active, s.created_at, s.updated_at,
                      (SELECT COUNT(*) FROM questions q WHERE q.subject_id = s.id AND q.is_active = 1) as question_count,
                      (SELECT COUNT(*) FROM exams e WHERE e.subject_id = s.id) as exam_count
               FROM subjects s
               WHERE s.id = ?;""",
            (subject_id,)
        )
        return dict_from_row(cursor.fetchone())

    @staticmethod
    def get_by_code(code: str) -> Optional[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM subjects WHERE UPPER(code) = ?;", (code.strip().upper(),))
        return dict_from_row(cursor.fetchone())

    @staticmethod
    def list_subjects(search: Optional[str] = None, department: Optional[str] = None,
                      is_active: Optional[bool] = None, teacher_id: Optional[str] = None,
                      offset: int = 0, limit: int = 50) -> Tuple[List[Dict[str, Any]], int]:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT s.id, s.code, s.name, s.description, s.department, s.is_active, s.created_at, s.updated_at,
                   (SELECT COUNT(*) FROM questions q WHERE q.subject_id = s.id AND q.is_active = 1) as question_count,
                   (SELECT COUNT(*) FROM exams e WHERE e.subject_id = s.id) as exam_count
            FROM subjects s
            WHERE 1=1
        """
        count_query = "SELECT COUNT(*) FROM subjects s WHERE 1=1"
        params = []

        if is_active is not None:
            filter_str = " AND s.is_active = ?"
            query += filter_str
            count_query += filter_str
            params.append(1 if is_active else 0)

        if department:
            filter_str = " AND LOWER(s.department) = ?"
            query += filter_str
            count_query += filter_str
            params.append(department.strip().lower())

        if teacher_id:
            filter_str = " AND s.id IN (SELECT subject_id FROM subject_teachers WHERE teacher_id = ?)"
            query += filter_str
            count_query += filter_str
            params.append(teacher_id)

        if search:
            s_param = f"%{search.strip().lower()}%"
            filter_str = " AND (LOWER(s.code) LIKE ? OR LOWER(s.name) LIKE ? OR LOWER(s.description) LIKE ?)"
            query += filter_str
            count_query += filter_str
            params.extend([s_param, s_param, s_param])

        cursor.execute(count_query, params)
        total = cursor.fetchone()[0]

        query += " ORDER BY s.code ASC LIMIT ? OFFSET ?;"
        cursor.execute(query, params + [limit, offset])
        items = list_from_rows(cursor.fetchall())
        return items, total

    @staticmethod
    def get_assigned_teachers(subject_id: str) -> List[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT st.teacher_id, st.assigned_at, t.teacher_id_code as teacher_code,
                      u.full_name as teacher_name, t.department
               FROM subject_teachers st
               JOIN teachers t ON st.teacher_id = t.id
               JOIN users u ON t.user_id = u.id
               WHERE st.subject_id = ?
               ORDER BY u.full_name ASC;""",
            (subject_id,)
        )
        return list_from_rows(cursor.fetchall())

    @staticmethod
    def create_subject(data: Dict[str, Any]) -> str:
        subject_id = str(uuid.uuid4())
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with transaction():
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO subjects (id, code, name, description, department, is_active, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, 1, ?, ?);""",
                (subject_id, data["code"].strip().upper(), data["name"].strip(),
                 data.get("description"), data.get("department"), now, now)
            )
        return subject_id

    @staticmethod
    def update_subject(subject_id: str, data: Dict[str, Any]):
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        fields = []
        params = []
        for key in ["name", "description", "department"]:
            if key in data and data[key] is not None:
                fields.append(f"{key} = ?")
                params.append(data[key])
        if "is_active" in data and data["is_active"] is not None:
            fields.append("is_active = ?")
            params.append(1 if data["is_active"] else 0)

        if not fields:
            return

        fields.append("updated_at = ?")
        params.append(now)
        params.append(subject_id)

        with transaction():
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(f"UPDATE subjects SET {', '.join(fields)} WHERE id = ?;", params)

    @staticmethod
    def assign_teacher(subject_id: str, teacher_id: str):
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with transaction():
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT OR IGNORE INTO subject_teachers (id, subject_id, teacher_id, assigned_at)
                   VALUES (?, ?, ?, ?);""",
                (str(uuid.uuid4()), subject_id, teacher_id, now)
            )

    @staticmethod
    def remove_teacher(subject_id: str, teacher_id: str):
        with transaction():
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM subject_teachers WHERE subject_id = ? AND teacher_id = ?;",
                (subject_id, teacher_id)
            )
