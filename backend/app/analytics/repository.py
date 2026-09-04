"""
ExamHub - Analytics Repository Layer
Executes optimized SQL queries to retrieve candidate scores, question attempt data,
proctoring records, and subject aggregates for psychometric analysis.
"""

from typing import List, Dict, Any, Optional, Tuple
from backend.app.database.connection import get_db_connection
from backend.app.core.logger import logger

class AnalyticsRepository:
    """Provides structured data access for psychometric and cohort evaluations."""

    @staticmethod
    def get_exam_metadata(exam_id: str) -> Optional[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.id, e.name, e.subject_id, e.teacher_id, e.description,
                   e.duration_minutes, e.total_marks, e.passing_percentage,
                   e.status, s.code as subject_code, s.name as subject_name
            FROM exams e
            JOIN subjects s ON e.subject_id = s.id
            WHERE e.id = ?
        """, (exam_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    @staticmethod
    def get_exam_student_scores(exam_id: str) -> List[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.id, r.attempt_id, r.exam_id, r.student_id, r.obtained_marks,
                   r.total_marks, r.percentage, r.grade, r.pass_fail, r.rank,
                   r.correct_count, r.wrong_count, r.unanswered_count,
                   ea.start_time, ea.end_time,
                   u.full_name, st.student_id_code as roll_number, u.id as user_id
            FROM results r
            JOIN exam_attempts ea ON r.attempt_id = ea.id
            JOIN students st ON r.student_id = st.id
            JOIN users u ON st.user_id = u.id
            WHERE r.exam_id = ?
            ORDER BY r.obtained_marks DESC
        """, (exam_id,))
        return [dict(r) for r in cursor.fetchall()]

    @staticmethod
    def get_exam_questions_with_answers(exam_id: str) -> List[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT q.id as question_id, eq.order_index, eq.marks_allocated,
                   q.question_text, q.difficulty, q.topic, q.correct_answer,
                   q.option_a, q.option_b, q.option_c, q.option_d,
                   sa.selected_option, sa.is_correct, sa.marks_obtained,
                   sa.attempt_id, r.obtained_marks as student_total_score
            FROM exam_questions eq
            JOIN questions q ON eq.question_id = q.id
            LEFT JOIN student_answers sa ON q.id = sa.question_id
            LEFT JOIN exam_attempts ea ON sa.attempt_id = ea.id AND ea.exam_id = ?
            LEFT JOIN results r ON ea.id = r.attempt_id
            WHERE eq.exam_id = ?
            ORDER BY eq.order_index ASC
        """, (exam_id, exam_id))
        return [dict(r) for r in cursor.fetchall()]

    @staticmethod
    def get_system_overview_counts() -> Dict[str, int]:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        counts = {}
        queries = {
            "total_users": "SELECT COUNT(*) FROM users",
            "total_students": "SELECT COUNT(*) FROM students",
            "total_teachers": "SELECT COUNT(*) FROM teachers",
            "total_subjects": "SELECT COUNT(*) FROM subjects WHERE is_active = 1",
            "total_questions": "SELECT COUNT(*) FROM questions WHERE is_active = 1",
            "total_exams": "SELECT COUNT(*) FROM exams",
            "total_attempts_completed": "SELECT COUNT(*) FROM exam_attempts WHERE status IN ('submitted', 'auto_submitted', 'evaluated')",
            "active_exams_count": "SELECT COUNT(*) FROM exams WHERE status = 'active'"
        }
        
        for key, query in queries.items():
            cursor.execute(query)
            counts[key] = cursor.fetchone()[0]
            
        cursor.execute("SELECT AVG(percentage) FROM results")
        avg_score = cursor.fetchone()[0]
        counts["global_average_score_pct"] = round(float(avg_score or 0.0), 2)

        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN pass_fail = 'PASS' THEN 1 ELSE 0 END) as passed
            FROM results
        """)
        row = cursor.fetchone()
        if row and row[0] and row[0] > 0:
            counts["global_pass_rate_pct"] = round((float(row[1] or 0) / float(row[0])) * 100.0, 2)
        else:
            counts["global_pass_rate_pct"] = 0.0

        cursor.execute("SELECT COUNT(*) FROM proctoring_logs WHERE DATE(timestamp) = DATE('now')")
        counts["proctoring_alerts_today"] = cursor.fetchone()[0]

        return counts

    @staticmethod
    def get_subject_performance_summaries() -> List[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.id as subject_id, s.code as subject_code, s.name as subject_name,
                   s.department,
                   COUNT(DISTINCT e.id) as total_exams,
                   COUNT(r.id) as total_candidates_evaluated,
                   COALESCE(AVG(r.percentage), 0.0) as overall_mean_percentage,
                   COALESCE(SUM(CASE WHEN r.pass_fail = 'PASS' THEN 1.0 ELSE 0.0 END) / NULLIF(COUNT(r.id), 0) * 100.0, 0.0) as overall_pass_rate
            FROM subjects s
            LEFT JOIN exams e ON s.id = e.subject_id
            LEFT JOIN results r ON e.id = r.exam_id
            WHERE s.is_active = 1
            GROUP BY s.id
            ORDER BY s.code ASC
        """)
        rows = cursor.fetchall()
        summaries = []
        for row in rows:
            d = dict(row)
            d["overall_mean_percentage"] = round(float(d["overall_mean_percentage"]), 2)
            d["overall_pass_rate"] = round(float(d["overall_pass_rate"]), 2)
            d["performance_trend"] = "Stable" if d["overall_pass_rate"] >= 60 else "Developing"
            summaries.append(d)
        return summaries
