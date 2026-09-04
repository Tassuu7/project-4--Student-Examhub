"""
ExamHub - JSON Exam Archive Exporter & Importer
Packages entire exams including question metadata, assignments, and test settings
into standardized JSON bundle archives.
"""

import json
from typing import Dict, Any, Optional
from datetime import datetime
from backend.app.database.connection import get_db_connection

class JsonArchiveExporter:
    """Exports and restores complete examination packages in JSON format."""

    @staticmethod
    def export_exam_package(exam_id: str) -> Dict[str, Any]:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1. Exam Info
        cursor.execute("SELECT * FROM exams WHERE id = ?", (exam_id,))
        exam_row = cursor.fetchone()
        if not exam_row:
            return {}

        exam_dict = dict(exam_row)

        # 2. Questions
        cursor.execute("""
            SELECT q.*, eq.order_index, eq.marks_allocated
            FROM exam_questions eq
            JOIN questions q ON eq.question_id = q.id
            WHERE eq.exam_id = ?
            ORDER BY eq.order_index ASC
        """, (exam_id,))
        questions = [dict(r) for r in cursor.fetchall()]

        # 3. Subject
        cursor.execute("SELECT * FROM subjects WHERE id = ?", (exam_dict["subject_id"],))
        subject_row = cursor.fetchone()
        subject_dict = dict(subject_row) if subject_row else {}

        package = {
            "schema_version": "examhub-archive-1.0",
            "exported_at": datetime.utcnow().isoformat(),
            "subject": subject_dict,
            "exam": exam_dict,
            "questions_count": len(questions),
            "questions": questions
        }

        return package
