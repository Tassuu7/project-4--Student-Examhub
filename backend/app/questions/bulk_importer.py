"""
ExamHub - Bulk Question Importer & Exporter (CSV Format)
"""

import csv
import io
from typing import List, Tuple, Dict, Any
from backend.app.questions.repository import QuestionRepository
from backend.app.subjects.repository import SubjectRepository
from backend.app.questions.schemas import BulkImportSummary
from backend.app.core.constants import QuestionDifficulty, CorrectOption

CSV_HEADER = [
    "SubjectCode", "QuestionText", "OptionA", "OptionB", "OptionC", "OptionD",
    "CorrectAnswer", "Marks", "Difficulty", "Topic", "Explanation"
]

class QuestionBulkService:
    @staticmethod
    def generate_csv_template() -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(CSV_HEADER)
        writer.writerow([
            "CS101",
            "Which built-in module in Python is used for regular expressions?",
            "regex", "pyregex", "re", "string",
            "C", "1.0", "Easy", "Standard Library",
            "The 're' module provides regular expression matching operations."
        ])
        return output.getvalue()

    @staticmethod
    def export_questions_to_csv(subject_id: str = None) -> str:
        questions, _ = QuestionRepository.list_questions(subject_id=subject_id, limit=5000)
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(CSV_HEADER)
        for q in questions:
            writer.writerow([
                q["subject_code"],
                q["question_text"],
                q["option_a"],
                q["option_b"],
                q["option_c"],
                q["option_d"],
                q["correct_answer"],
                q["marks"],
                q["difficulty"],
                q.get("topic") or "",
                q.get("explanation") or ""
            ])
        return output.getvalue()

    @staticmethod
    def import_questions_from_csv(csv_content: str, default_teacher_id: str = None) -> BulkImportSummary:
        reader = csv.DictReader(io.StringIO(csv_content))
        total = 0
        imported = 0
        errors = []

        # Cache subjects by code
        subjects, _ = SubjectRepository.list_subjects(limit=1000)
        subject_code_map = {s["code"].upper(): s["id"] for s in subjects}

        for idx, row in enumerate(reader, start=2): # Line 2 is first data row
            total += 1
            sub_code = (row.get("SubjectCode") or "").strip().upper()
            q_text = (row.get("QuestionText") or "").strip()
            oa = (row.get("OptionA") or "").strip()
            ob = (row.get("OptionB") or "").strip()
            oc = (row.get("OptionC") or "").strip()
            od = (row.get("OptionD") or "").strip()
            ans = (row.get("CorrectAnswer") or "").strip().upper()
            marks_str = (row.get("Marks") or "1.0").strip()
            diff_str = (row.get("Difficulty") or "Medium").strip().capitalize()
            topic = (row.get("Topic") or "").strip() or None
            expl = (row.get("Explanation") or "").strip() or None

            # Validation
            if not sub_code or sub_code not in subject_code_map:
                errors.append(f"Row {idx}: Unknown SubjectCode '{sub_code}'")
                continue

            if not q_text:
                errors.append(f"Row {idx}: Missing QuestionText")
                continue

            if not (oa and ob and oc and od):
                errors.append(f"Row {idx}: All four options (A, B, C, D) are required")
                continue

            if ans not in ["A", "B", "C", "D"]:
                errors.append(f"Row {idx}: Invalid CorrectAnswer '{ans}'. Must be A, B, C, or D")
                continue

            try:
                marks = float(marks_str)
                if marks <= 0:
                    raise ValueError()
            except ValueError:
                errors.append(f"Row {idx}: Invalid Marks value '{marks_str}'. Must be a positive number")
                continue

            if diff_str not in ["Easy", "Medium", "Hard"]:
                diff_str = "Medium"

            QuestionRepository.create_question({
                "subject_id": subject_code_map[sub_code],
                "teacher_id": default_teacher_id,
                "question_text": q_text,
                "option_a": oa,
                "option_b": ob,
                "option_c": oc,
                "option_d": od,
                "correct_answer": ans,
                "marks": marks,
                "difficulty": diff_str,
                "topic": topic,
                "explanation": expl
            })
            imported += 1

        return BulkImportSummary(
            total_processed=total,
            imported_count=imported,
            failed_count=len(errors),
            errors=errors
        )
