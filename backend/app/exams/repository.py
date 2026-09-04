"""
ExamHub - Exam Engine Database Repository
"""

import uuid
import datetime
from typing import Optional, List, Dict, Any, Tuple
from backend.app.database.connection import get_db_connection, transaction
from backend.app.core.constants import ExamStatus, AttemptStatus, EvaluationResult

class ExamRepository:
    @staticmethod
    def create_exam(data: Dict[str, Any]) -> str:
        exam_id = str(uuid.uuid4())
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with transaction():
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO exams (
                    id, name, subject_id, teacher_id, description, duration_minutes,
                    total_marks, passing_percentage, start_date, end_date, instructions,
                    status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
                (
                    exam_id,
                    data["name"].strip(),
                    data["subject_id"],
                    data["teacher_id"],
                    data.get("description"),
                    int(data["duration_minutes"]),
                    float(data.get("total_marks", 0.0)),
                    float(data.get("passing_percentage", 40.0)),
                    data["start_date"],
                    data["end_date"],
                    data.get("instructions"),
                    data.get("status", ExamStatus.DRAFT.value),
                    now,
                    now
                )
            )
        return exam_id

    @staticmethod
    def update_exam(exam_id: str, data: Dict[str, Any]) -> bool:
        if not data:
            return False
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        fields = []
        values = []
        for k, v in data.items():
            if k in ["name", "subject_id", "teacher_id", "description", "duration_minutes",
                     "total_marks", "passing_percentage", "start_date", "end_date",
                     "instructions", "status"]:
                fields.append(f"{k} = ?")
                values.append(v)
        fields.append("updated_at = ?")
        values.append(now)
        values.append(exam_id)

        with transaction():
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(f"UPDATE exams SET {', '.join(fields)} WHERE id = ?;", tuple(values))
            return cursor.rowcount > 0

    @staticmethod
    def get_by_id(exam_id: str) -> Optional[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT e.*, s.code as subject_code, s.name as subject_name,
                      u.full_name as teacher_name,
                      (SELECT COUNT(*) FROM exam_questions WHERE exam_id = e.id) as question_count,
                      (SELECT COUNT(*) FROM exam_assignments WHERE exam_id = e.id) as assigned_students_count,
                      (SELECT COUNT(*) FROM exam_attempts WHERE exam_id = e.id AND status IN ('submitted', 'auto_submitted', 'evaluated')) as completed_attempts_count
               FROM exams e
               JOIN subjects s ON e.subject_id = s.id
               JOIN teachers t ON e.teacher_id = t.id
               JOIN users u ON t.user_id = u.id
               WHERE e.id = ?;""",
            (exam_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    @staticmethod
    def list_exams(
        subject_id: Optional[str] = None,
        teacher_id: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
        offset: int = 0,
        limit: int = 20
    ) -> Tuple[List[Dict[str, Any]], int]:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT e.*, s.code as subject_code, s.name as subject_name,
                   u.full_name as teacher_name,
                   (SELECT COUNT(*) FROM exam_questions WHERE exam_id = e.id) as question_count,
                   (SELECT COUNT(*) FROM exam_assignments WHERE exam_id = e.id) as assigned_students_count,
                   (SELECT COUNT(*) FROM exam_attempts WHERE exam_id = e.id AND status IN ('submitted', 'auto_submitted', 'evaluated')) as completed_attempts_count
            FROM exams e
            JOIN subjects s ON e.subject_id = s.id
            JOIN teachers t ON e.teacher_id = t.id
            JOIN users u ON t.user_id = u.id
            WHERE 1=1
        """
        count_query = """
            SELECT COUNT(*)
            FROM exams e
            JOIN subjects s ON e.subject_id = s.id
            JOIN teachers t ON e.teacher_id = t.id
            JOIN users u ON t.user_id = u.id
            WHERE 1=1
        """
        params = []
        if subject_id:
            query += " AND e.subject_id = ?"
            count_query += " AND e.subject_id = ?"
            params.append(subject_id)
        if teacher_id:
            query += " AND e.teacher_id = ?"
            count_query += " AND e.teacher_id = ?"
            params.append(teacher_id)
        if status:
            query += " AND e.status = ?"
            count_query += " AND e.status = ?"
            params.append(status)
        if search:
            query += " AND (e.name LIKE ? OR s.code LIKE ? OR s.name LIKE ?)"
            count_query += " AND (e.name LIKE ? OR s.code LIKE ? OR s.name LIKE ?)"
            like_term = f"%{search.strip()}%"
            params.extend([like_term, like_term, like_term])

        cursor.execute(count_query, tuple(params))
        total = cursor.fetchone()[0]

        query += " ORDER BY e.created_at DESC LIMIT ? OFFSET ?"
        exec_params = list(params)
        exec_params.extend([limit, offset])

        cursor.execute(query, tuple(exec_params))
        rows = cursor.fetchall()
        return [dict(r) for r in rows], total

    @staticmethod
    def delete_exam(exam_id: str) -> bool:
        with transaction():
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM exams WHERE id = ?;", (exam_id,))
            return cursor.rowcount > 0

    # Question Associations
    @staticmethod
    def set_exam_questions(exam_id: str, question_allocations: List[Dict[str, Any]]) -> float:
        """Replace all question allocations for an exam and compute total marks."""
        with transaction():
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM exam_questions WHERE exam_id = ?;", (exam_id,))
            total_marks = 0.0
            for idx, item in enumerate(question_allocations, start=1):
                eq_id = str(uuid.uuid4())
                marks = float(item.get("marks_allocated", 1.0))
                total_marks += marks
                cursor.execute(
                    """INSERT INTO exam_questions (id, exam_id, question_id, order_index, marks_allocated)
                       VALUES (?, ?, ?, ?, ?);""",
                    (eq_id, exam_id, item["question_id"], idx, marks)
                )
            cursor.execute("UPDATE exams SET total_marks = ? WHERE id = ?;", (total_marks, exam_id))
            return total_marks

    @staticmethod
    def get_exam_questions(exam_id: str) -> List[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT eq.id as exam_question_id, eq.order_index, eq.marks_allocated,
                      q.id as question_id, q.question_text, q.option_a, q.option_b,
                      q.option_c, q.option_d, q.correct_answer, q.marks as default_marks,
                      q.difficulty, q.topic, q.explanation
               FROM exam_questions eq
               JOIN questions q ON eq.question_id = q.id
               WHERE eq.exam_id = ?
               ORDER BY eq.order_index ASC;""",
            (exam_id,)
        )
        return [dict(r) for r in cursor.fetchall()]

    # Student Assignment
    @staticmethod
    def set_exam_students(exam_id: str, student_ids: List[str]) -> int:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with transaction():
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM exam_assignments WHERE exam_id = ?;", (exam_id,))
            count = 0
            for sid in student_ids:
                aid = str(uuid.uuid4())
                cursor.execute(
                    """INSERT INTO exam_assignments (id, exam_id, student_id, assigned_at, can_attempt, attempts_allowed)
                       VALUES (?, ?, ?, ?, 1, 1);""",
                    (aid, exam_id, sid, now)
                )
                count += 1
            return count

    @staticmethod
    def get_exam_assigned_students(exam_id: str) -> List[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT ea.id as assignment_id, ea.assigned_at, ea.can_attempt,
                      st.id as student_id, st.student_id_code as student_roll_number, st.grade_level,
                      u.id as user_id, u.full_name, u.email,
                      att.id as attempt_id, att.status as attempt_status,
                      res.obtained_marks, res.percentage, res.grade, res.pass_fail
               FROM exam_assignments ea
               JOIN students st ON ea.student_id = st.id
               JOIN users u ON st.user_id = u.id
               LEFT JOIN exam_attempts att ON att.exam_id = ea.exam_id AND att.student_id = ea.student_id
               LEFT JOIN results res ON res.attempt_id = att.id
               WHERE ea.exam_id = ?
               ORDER BY st.student_id_code ASC;""",
            (exam_id,)
        )
        return [dict(r) for r in cursor.fetchall()]

    @staticmethod
    def get_all_student_ids() -> List[str]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM students;")
        return [row[0] for row in cursor.fetchall()]

    @staticmethod
    def get_student_assigned_exams(student_id: str) -> List[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT e.*, s.code as subject_code, s.name as subject_name,
                      u.full_name as teacher_name,
                      (SELECT COUNT(*) FROM exam_questions WHERE exam_id = e.id) as question_count,
                      COALESCE(ea.can_attempt, 1) as can_attempt,
                      COALESCE(ea.attempts_allowed, 1) as attempts_allowed,
                      att.id as attempt_id, att.status as attempt_status,
                      att.time_remaining_seconds, att.start_time, att.end_time,
                      res.obtained_marks, res.percentage, res.grade, res.pass_fail, res.rank
               FROM exams e
               JOIN subjects s ON e.subject_id = s.id
               JOIN teachers t ON e.teacher_id = t.id
               JOIN users u ON t.user_id = u.id
               LEFT JOIN exam_assignments ea ON ea.exam_id = e.id AND ea.student_id = ?
               LEFT JOIN exam_attempts att ON att.exam_id = e.id AND att.student_id = ?
               LEFT JOIN results res ON res.attempt_id = att.id
               WHERE (ea.student_id = ? OR e.status IN ('active', 'scheduled', 'completed'))
                 AND e.status != 'cancelled'
               ORDER BY e.start_date DESC;""",
            (student_id, student_id, student_id)
        )
        return [dict(r) for r in cursor.fetchall()]

    # Attempts & Taking Exam
    @staticmethod
    def create_attempt(exam_id: str, student_id: str, duration_minutes: int) -> str:
        attempt_id = str(uuid.uuid4())
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        time_remaining_seconds = duration_minutes * 60
        with transaction():
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO exam_attempts (
                    id, exam_id, student_id, start_time, time_remaining_seconds,
                    status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, 'in_progress', ?, ?);""",
                (attempt_id, exam_id, student_id, now, time_remaining_seconds, now, now)
            )
        return attempt_id

    @staticmethod
    def get_attempt_by_id(attempt_id: str) -> Optional[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT att.*, e.name as exam_name, e.duration_minutes, e.total_marks,
                      e.passing_percentage, e.instructions, e.status as exam_status,
                      s.code as subject_code, s.name as subject_name,
                      st.student_id_code as student_roll_number, u.full_name as student_name
               FROM exam_attempts att
               JOIN exams e ON att.exam_id = e.id
               JOIN subjects s ON e.subject_id = s.id
               JOIN students st ON att.student_id = st.id
               JOIN users u ON st.user_id = u.id
               WHERE att.id = ?;""",
            (attempt_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    @staticmethod
    def get_student_attempt_for_exam(exam_id: str, student_id: str) -> Optional[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT * FROM exam_attempts WHERE exam_id = ? AND student_id = ?;""",
            (exam_id, student_id)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    @staticmethod
    def update_attempt_time(attempt_id: str, time_remaining_seconds: int):
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with transaction():
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE exam_attempts SET time_remaining_seconds = ?, updated_at = ? WHERE id = ?;""",
                (max(0, time_remaining_seconds), now, attempt_id)
            )

    @staticmethod
    def update_attempt_status(
        attempt_id: str,
        status: str,
        end_time: Optional[str] = None
    ):
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        end_val = end_time or now
        with transaction():
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE exam_attempts SET status = ?, end_time = ?, updated_at = ? WHERE id = ?;""",
                (status, end_val, now, attempt_id)
            )

    # Student Answers
    @staticmethod
    def upsert_student_answer(
        attempt_id: str,
        question_id: str,
        selected_option: Optional[str],
        is_marked_for_review: bool
    ):
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        answer_id = str(uuid.uuid4())
        review_flag = 1 if is_marked_for_review else 0
        with transaction():
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO student_answers (
                    id, attempt_id, question_id, selected_option, is_marked_for_review, saved_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(attempt_id, question_id) DO UPDATE SET
                    selected_option = excluded.selected_option,
                    is_marked_for_review = excluded.is_marked_for_review,
                    saved_at = excluded.saved_at;""",
                (answer_id, attempt_id, question_id, selected_option, review_flag, now)
            )

    @staticmethod
    def get_student_answers(attempt_id: str) -> Dict[str, Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT * FROM student_answers WHERE attempt_id = ?;""",
            (attempt_id,)
        )
        return {r["question_id"]: dict(r) for r in cursor.fetchall()}

    # Results & Evaluation
    @staticmethod
    def save_result(data: Dict[str, Any]) -> str:
        result_id = str(uuid.uuid4())
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with transaction():
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO results (
                    id, attempt_id, exam_id, student_id, total_questions,
                    correct_count, wrong_count, unanswered_count, total_marks,
                    obtained_marks, percentage, grade, pass_fail, rank, generated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
                (
                    result_id,
                    data["attempt_id"],
                    data["exam_id"],
                    data["student_id"],
                    int(data["total_questions"]),
                    int(data["correct_count"]),
                    int(data["wrong_count"]),
                    int(data["unanswered_count"]),
                    float(data["total_marks"]),
                    float(data["obtained_marks"]),
                    float(data["percentage"]),
                    data["grade"],
                    data["pass_fail"],
                    data.get("rank"),
                    now
                )
            )
            # Update attempt scores
            cursor.execute(
                """UPDATE exam_attempts SET
                    total_score = ?, percentage = ?, grade = ?, result = ?, evaluated_at = ?
                   WHERE id = ?;""",
                (
                    float(data["obtained_marks"]),
                    float(data["percentage"]),
                    data["grade"],
                    data["pass_fail"],
                    now,
                    data["attempt_id"]
                )
            )
        return result_id

    @staticmethod
    def update_student_answer_evaluation(attempt_id: str, question_id: str, is_correct: bool, marks_obtained: float):
        with transaction():
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE student_answers SET is_correct = ?, marks_obtained = ?
                   WHERE attempt_id = ? AND question_id = ?;""",
                (1 if is_correct else 0, marks_obtained, attempt_id, question_id)
            )

    @staticmethod
    def get_result_by_attempt_id(attempt_id: str) -> Optional[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT r.*, e.name as exam_name, s.code as subject_code, s.name as subject_name,
                      st.student_id_code as student_roll_number, u.full_name as student_name,
                      att.start_time, att.end_time
               FROM results r
               JOIN exams e ON r.exam_id = e.id
               JOIN subjects s ON e.subject_id = s.id
               JOIN students st ON r.student_id = st.id
               JOIN users u ON st.user_id = u.id
               JOIN exam_attempts att ON r.attempt_id = att.id
               WHERE r.attempt_id = ?;""",
            (attempt_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    @staticmethod
    def list_exam_results(exam_id: str) -> List[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT r.*, e.name as exam_name, s.code as subject_code, s.name as subject_name,
                      st.student_id_code as student_roll_number, u.full_name as student_name,
                      att.start_time, att.end_time
               FROM results r
               JOIN exams e ON r.exam_id = e.id
               JOIN subjects s ON e.subject_id = s.id
               JOIN students st ON r.student_id = st.id
               JOIN users u ON st.user_id = u.id
               JOIN exam_attempts att ON r.attempt_id = att.id
               WHERE r.exam_id = ?
               ORDER BY r.obtained_marks DESC, r.percentage DESC;""",
            (exam_id,)
        )
        return [dict(r) for r in cursor.fetchall()]

    @staticmethod
    def recalculate_exam_ranks(exam_id: str):
        """Calculates and updates ranks for all evaluated candidates of an exam."""
        results = ExamRepository.list_exam_results(exam_id)
        if not results:
            return
        with transaction():
            conn = get_db_connection()
            cursor = conn.cursor()
            current_rank = 1
            for idx, r in enumerate(results):
                # Standard dense or ordinal ranking
                cursor.execute("UPDATE results SET rank = ? WHERE id = ?;", (idx + 1, r["id"]))

    # Proctoring Event Logs
    @staticmethod
    def log_proctoring_event(attempt_id: str, event_type: str, details: Optional[str] = None):
        event_id = str(uuid.uuid4())
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with transaction():
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO proctoring_logs (id, attempt_id, event_type, details, timestamp)
                   VALUES (?, ?, ?, ?, ?);""",
                (event_id, attempt_id, event_type, details, now)
            )

    @staticmethod
    def get_proctoring_logs(attempt_id: str) -> List[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT * FROM proctoring_logs WHERE attempt_id = ? ORDER BY timestamp ASC;""",
            (attempt_id,)
        )
        return [dict(r) for r in cursor.fetchall()]
