"""
ExamHub - Student Feedback Database Repository
"""

import uuid
import datetime
from typing import List, Optional, Dict, Any
from backend.app.database.connection import get_db_connection, transaction

class FeedbackRepository:
    @staticmethod
    def create_or_update(exam_id: str, student_id: str, teacher_id: str, feedback_text: str, rating: int = 5, attempt_id: Optional[str] = None) -> Dict[str, Any]:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check existing
        cursor.execute(
            """SELECT id FROM student_feedbacks WHERE exam_id = ? AND student_id = ?;""",
            (exam_id, student_id)
        )
        row = cursor.fetchone()

        with transaction():
            if row:
                fid = row[0]
                cursor.execute(
                    """UPDATE student_feedbacks
                       SET feedback_text = ?, rating = ?, teacher_id = ?, attempt_id = COALESCE(?, attempt_id), updated_at = ?
                       WHERE id = ?;""",
                    (feedback_text, rating, teacher_id, attempt_id, now, fid)
                )
            else:
                fid = str(uuid.uuid4())
                cursor.execute(
                    """INSERT INTO student_feedbacks (id, exam_id, student_id, teacher_id, attempt_id, feedback_text, rating, created_at, updated_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);""",
                    (fid, exam_id, student_id, teacher_id, attempt_id, feedback_text, rating, now, now)
                )

        return FeedbackRepository.get_by_id(fid)

    @staticmethod
    def get_by_id(feedback_id: str) -> Optional[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT f.*,
                      e.name as exam_name,
                      s.code as subject_code, s.name as subject_name,
                      u_stu.full_name as student_name, st.student_id_code as student_roll_number,
                      u_tch.full_name as teacher_name
               FROM student_feedbacks f
               JOIN exams e ON f.exam_id = e.id
               JOIN subjects s ON e.subject_id = s.id
               JOIN students st ON f.student_id = st.id
               JOIN users u_stu ON st.user_id = u_stu.id
               JOIN teachers t ON f.teacher_id = t.id
               JOIN users u_tch ON t.user_id = u_tch.id
               WHERE f.id = ?;""",
            (feedback_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    @staticmethod
    def list_by_student(student_id: str) -> List[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT f.*,
                      e.name as exam_name,
                      s.code as subject_code, s.name as subject_name,
                      u_stu.full_name as student_name, st.student_id_code as student_roll_number,
                      u_tch.full_name as teacher_name
               FROM student_feedbacks f
               JOIN exams e ON f.exam_id = e.id
               JOIN subjects s ON e.subject_id = s.id
               JOIN students st ON f.student_id = st.id
               JOIN users u_stu ON st.user_id = u_stu.id
               JOIN teachers t ON f.teacher_id = t.id
               JOIN users u_tch ON t.user_id = u_tch.id
               WHERE f.student_id = ?
               ORDER BY f.created_at DESC;""",
            (student_id,)
        )
        return [dict(r) for r in cursor.fetchall()]

    @staticmethod
    def list_by_exam(exam_id: str) -> List[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT f.*,
                      e.name as exam_name,
                      s.code as subject_code, s.name as subject_name,
                      u_stu.full_name as student_name, st.student_id_code as student_roll_number,
                      u_tch.full_name as teacher_name
               FROM student_feedbacks f
               JOIN exams e ON f.exam_id = e.id
               JOIN subjects s ON e.subject_id = s.id
               JOIN students st ON f.student_id = st.id
               JOIN users u_stu ON st.user_id = u_stu.id
               JOIN teachers t ON f.teacher_id = t.id
               JOIN users u_tch ON t.user_id = u_tch.id
               WHERE f.exam_id = ?
               ORDER BY f.created_at DESC;""",
            (exam_id,)
        )
        return [dict(r) for r in cursor.fetchall()]

    @staticmethod
    def list_all() -> List[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT f.*,
                      e.name as exam_name,
                      s.code as subject_code, s.name as subject_name,
                      u_stu.full_name as student_name, st.student_id_code as student_roll_number,
                      u_tch.full_name as teacher_name
               FROM student_feedbacks f
               JOIN exams e ON f.exam_id = e.id
               JOIN subjects s ON e.subject_id = s.id
               JOIN students st ON f.student_id = st.id
               JOIN users u_stu ON st.user_id = u_stu.id
               JOIN teachers t ON f.teacher_id = t.id
               JOIN users u_tch ON t.user_id = u_tch.id
               ORDER BY f.created_at DESC;"""
        )
        return [dict(r) for r in cursor.fetchall()]
