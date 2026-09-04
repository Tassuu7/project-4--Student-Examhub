"""
ExamHub - Excel-Compatible CSV Exporter
Formats examination rosters, student scorecards, and item response logs
into UTF-8 BOM CSV files for academic record-keeping.
"""

import csv
import io
from typing import List, Dict, Any
from backend.app.database.connection import get_db_connection

class CsvExporter:
    """Generates standard CSV exports for academic administration."""

    @staticmethod
    def export_exam_results_csv(exam_id: str) -> str:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.name as exam_name, s.code as subject_code, s.name as subject_name
            FROM exams e
            JOIN subjects s ON e.subject_id = s.id
            WHERE e.id = ?
        """, (exam_id,))
        exam_meta = cursor.fetchone()

        cursor.execute("""
            SELECT r.rank, st.student_id_code as roll_number, u.full_name as student_name,
                   u.email, r.obtained_marks, r.total_marks, r.percentage,
                   r.grade, r.pass_fail, r.correct_count, r.wrong_count,
                   r.unanswered_count, ea.start_time, ea.end_time
            FROM results r
            JOIN exam_attempts ea ON r.attempt_id = ea.id
            JOIN students st ON r.student_id = st.id
            JOIN users u ON st.user_id = u.id
            WHERE r.exam_id = ?
            ORDER BY r.rank ASC
        """, (exam_id,))
        rows = [dict(r) for r in cursor.fetchall()]

        output = io.StringIO()
        # UTF-8 BOM for proper Excel Unicode detection
        output.write('\ufeff')
        writer = csv.writer(output)

        # Meta Header
        writer.writerow(["ExamHub Academic Score Report"])
        if exam_meta:
            writer.writerow(["Exam Title", exam_meta["exam_name"]])
            writer.writerow(["Subject", f"{exam_meta['subject_code']} - {exam_meta['subject_name']}"])
        writer.writerow([])

        # Table Header
        writer.writerow([
            "Rank", "Roll Number", "Student Name", "Email",
            "Obtained Marks", "Total Marks", "Percentage (%)",
            "Grade", "Outcome", "Correct", "Wrong", "Skipped",
            "Start Time", "Submission Time"
        ])

        for r in rows:
            writer.writerow([
                r["rank"],
                r["roll_number"],
                r["student_name"],
                r["email"],
                r["obtained_marks"],
                r["total_marks"],
                f"{r['percentage']:.2f}",
                r["grade"],
                r["pass_fail"],
                r["correct_count"],
                r["wrong_count"],
                r["unanswered_count"],
                r.get("start_time", ""),
                r.get("end_time", "")
            ])

        return output.getvalue()

    @staticmethod
    def export_question_bank_csv(subject_id: str) -> str:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT q.id, q.question_text, q.option_a, q.option_b, q.option_c, q.option_d,
                   q.correct_answer, q.marks, q.difficulty, q.topic, q.explanation
            FROM questions q
            WHERE q.subject_id = ? AND q.is_active = 1
            ORDER BY q.created_at ASC
        """, (subject_id,))
        rows = [dict(r) for r in cursor.fetchall()]

        output = io.StringIO()
        output.write('\ufeff')
        writer = csv.writer(output)

        writer.writerow([
            "Question ID", "Question Text", "Option A", "Option B",
            "Option C", "Option D", "Correct Answer", "Marks",
            "Difficulty", "Topic", "Explanation"
        ])

        for r in rows:
            writer.writerow([
                r["id"],
                r["question_text"],
                r["option_a"],
                r["option_b"],
                r["option_c"],
                r["option_d"],
                r["correct_answer"],
                r["marks"],
                r["difficulty"],
                r.get("topic", ""),
                r.get("explanation", "")
            ])

        return output.getvalue()
