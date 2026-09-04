"""
ExamHub - Grade Moderation & Audit Trail
Handles teacher remark requests, manual score overrides, and grade change audit histories.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from backend.app.database.connection import get_db_connection

class GradeModerationManager:
    """Manages teacher manual scoring adjustments with audit tracking."""

    @staticmethod
    def adjust_student_score(
        attempt_id: str,
        question_id: str,
        new_marks: float,
        reason: str,
        moderator_user_id: str
    ) -> Dict[str, Any]:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Update student_answers
        cursor.execute("""
            UPDATE student_answers
            SET marks_obtained = ?,
                is_correct = CASE WHEN ? > 0 THEN 1 ELSE 0 END
            WHERE attempt_id = ? AND question_id = ?
        """, (new_marks, new_marks, attempt_id, question_id))

        # Recalculate total obtained marks
        cursor.execute("""
            SELECT SUM(marks_obtained) FROM student_answers WHERE attempt_id = ?
        """, (attempt_id,))
        total_obtained = float(cursor.fetchone()[0] or 0.0)

        cursor.execute("SELECT total_marks, exam_id FROM results WHERE attempt_id = ?", (attempt_id,))
        res_info = cursor.fetchone()
        if res_info:
            total_marks = float(res_info[0])
            new_pct = (total_obtained / total_marks * 100.0) if total_marks > 0 else 0.0

            # Compute new letter grade
            if new_pct >= 90:
                grade = "A+"
            elif new_pct >= 80:
                grade = "A"
            elif new_pct >= 70:
                grade = "B+"
            elif new_pct >= 60:
                grade = "B"
            elif new_pct >= 50:
                grade = "C"
            elif new_pct >= 40:
                grade = "D"
            else:
                grade = "F"

            pass_fail = "PASS" if new_pct >= 40.0 else "FAIL"

            cursor.execute("""
                UPDATE results
                SET obtained_marks = ?, percentage = ?, grade = ?, pass_fail = ?
                WHERE attempt_id = ?
            """, (total_obtained, round(new_pct, 2), grade, pass_fail, attempt_id))

        # Log to audit_logs
        import uuid
        cursor.execute("""
            INSERT INTO audit_logs (id, user_id, action, entity_type, entity_id, details_json, created_at)
            VALUES (?, ?, 'GRADE_MODERATION', 'attempt', ?, ?, ?)
        """, (
            str(uuid.uuid4()), moderator_user_id, attempt_id,
            f'{{"question_id":"{question_id}","new_marks":{new_marks},"reason":"{reason}"}}',
            datetime.utcnow().isoformat()
        ))

        conn.commit()

        return {
            "attempt_id": attempt_id,
            "new_obtained_marks": total_obtained,
            "status": "updated",
            "moderated_by": moderator_user_id
        }
