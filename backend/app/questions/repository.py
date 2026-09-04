"""
ExamHub - Question Bank Data Access Repository
"""

import uuid
import datetime
from typing import Optional, List, Dict, Any, Tuple
from backend.app.database.connection import get_db_connection, dict_from_row, list_from_rows, transaction
from backend.app.core.constants import QuestionDifficulty

class QuestionRepository:
    @staticmethod
    def get_by_id(question_id: str) -> Optional[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT q.id, q.subject_id, q.teacher_id, q.question_text,
                      q.option_a, q.option_b, q.option_c, q.option_d,
                      q.correct_answer, q.marks, q.difficulty, q.topic, q.explanation,
                      q.is_active, q.created_at, q.updated_at,
                      s.code as subject_code, s.name as subject_name,
                      u.full_name as teacher_name,
                      (SELECT COUNT(*) FROM exam_questions eq WHERE eq.question_id = q.id) as used_in_exam_count
               FROM questions q
               JOIN subjects s ON q.subject_id = s.id
               LEFT JOIN teachers t ON q.teacher_id = t.id
               LEFT JOIN users u ON t.user_id = u.id
               WHERE q.id = ?;""",
            (question_id,)
        )
        return dict_from_row(cursor.fetchone())

    @staticmethod
    def list_questions(subject_id: Optional[str] = None,
                       difficulty: Optional[QuestionDifficulty] = None,
                       topic: Optional[str] = None,
                       search: Optional[str] = None,
                       teacher_id: Optional[str] = None,
                       is_active: Optional[bool] = True,
                       offset: int = 0, limit: int = 20) -> Tuple[List[Dict[str, Any]], int]:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT q.id, q.subject_id, q.teacher_id, q.question_text,
                   q.option_a, q.option_b, q.option_c, q.option_d,
                   q.correct_answer, q.marks, q.difficulty, q.topic, q.explanation,
                   q.is_active, q.created_at, q.updated_at,
                   s.code as subject_code, s.name as subject_name,
                   u.full_name as teacher_name,
                   (SELECT COUNT(*) FROM exam_questions eq WHERE eq.question_id = q.id) as used_in_exam_count
            FROM questions q
            JOIN subjects s ON q.subject_id = s.id
            LEFT JOIN teachers t ON q.teacher_id = t.id
            LEFT JOIN users u ON t.user_id = u.id
            WHERE 1=1
        """
        count_query = "SELECT COUNT(*) FROM questions q JOIN subjects s ON q.subject_id = s.id WHERE 1=1"
        params = []

        if subject_id:
            query += " AND q.subject_id = ?"
            count_query += " AND q.subject_id = ?"
            params.append(subject_id)

        if difficulty:
            query += " AND q.difficulty = ?"
            count_query += " AND q.difficulty = ?"
            params.append(difficulty.value)

        if topic:
            query += " AND LOWER(q.topic) = ?"
            count_query += " AND LOWER(q.topic) = ?"
            params.append(topic.strip().lower())

        if teacher_id:
            query += " AND q.teacher_id = ?"
            count_query += " AND q.teacher_id = ?"
            params.append(teacher_id)

        if is_active is not None:
            query += " AND q.is_active = ?"
            count_query += " AND q.is_active = ?"
            params.append(1 if is_active else 0)

        if search:
            s_param = f"%{search.strip().lower()}%"
            filter_str = " AND (LOWER(q.question_text) LIKE ? OR LOWER(q.topic) LIKE ? OR LOWER(q.explanation) LIKE ?)"
            query += filter_str
            count_query += filter_str
            params.extend([s_param, s_param, s_param])

        cursor.execute(count_query, params)
        total = cursor.fetchone()[0]

        query += " ORDER BY q.created_at DESC LIMIT ? OFFSET ?;"
        cursor.execute(query, params + [limit, offset])
        items = list_from_rows(cursor.fetchall())
        return items, total

    @staticmethod
    def create_question(data: Dict[str, Any]) -> str:
        question_id = str(uuid.uuid4())
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with transaction():
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO questions (
                    id, subject_id, teacher_id, question_text, option_a, option_b, option_c, option_d,
                    correct_answer, marks, difficulty, topic, explanation, is_active, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?);""",
                (
                    question_id,
                    data["subject_id"],
                    data.get("teacher_id"),
                    data["question_text"].strip(),
                    data["option_a"].strip(),
                    data["option_b"].strip(),
                    data["option_c"].strip(),
                    data["option_d"].strip(),
                    data["correct_answer"],
                    float(data.get("marks", 1.0)),
                    data.get("difficulty", "Medium"),
                    data.get("topic"),
                    data.get("explanation"),
                    now,
                    now
                )
            )
        return question_id

    @staticmethod
    def update_question(question_id: str, data: Dict[str, Any]):
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        fields = []
        params = []
        updatable = [
            "subject_id", "question_text", "option_a", "option_b", "option_c", "option_d",
            "correct_answer", "marks", "difficulty", "topic", "explanation"
        ]
        for key in updatable:
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
        params.append(question_id)

        with transaction():
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(f"UPDATE questions SET {', '.join(fields)} WHERE id = ?;", params)

    @staticmethod
    def delete_question(question_id: str):
        with transaction():
            conn = get_db_connection()
            cursor = conn.cursor()
            # If used in exams, soft delete to preserve historical integrity
            cursor.execute("SELECT COUNT(*) FROM exam_questions WHERE question_id = ?;", (question_id,))
            count = cursor.fetchone()[0]
            if count > 0:
                cursor.execute("UPDATE questions SET is_active = 0 WHERE id = ?;", (question_id,))
            else:
                cursor.execute("DELETE FROM questions WHERE id = ?;", (question_id,))

    @staticmethod
    def get_topics_for_subject(subject_id: str) -> List[str]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT DISTINCT topic FROM questions
               WHERE subject_id = ? AND topic IS NOT NULL AND topic != ''
               ORDER BY topic ASC;""",
            (subject_id,)
        )
        return [r[0] for r in cursor.fetchall()]
