"""
ExamHub - Aiken Question Format Parser & Ingestion Engine
Parses standard human-readable Aiken text syntax into structured question models.
Format:
Question text here
A. Option A
B. Option B
C. Option C
D. Option D
ANSWER: A
"""

import re
import uuid
from datetime import datetime
from typing import List, Dict, Any, Tuple
from backend.app.database.connection import get_db_connection

class AikenParser:
    """Parses text in standard Aiken syntax and persists valid questions."""

    @staticmethod
    def parse_aiken_string(raw_text: str) -> Tuple[List[Dict[str, Any]], List[str]]:
        lines = [line.strip() for line in raw_text.strip().split('\n')]
        parsed_questions = []
        errors = []

        current_q = {}
        options_found = {}

        i = 0
        while i < len(lines):
            line = lines[i]
            if not line:
                i += 1
                continue

            # Check if this is the start of a question
            question_text = line
            i += 1

            options_found = {}
            # Collect options A, B, C, D
            while i < len(lines) and re.match(r'^[A-D][\.\)]\s+', lines[i]):
                opt_match = re.match(r'^([A-D])[\.\)]\s+(.*)$', lines[i])
                if opt_match:
                    opt_letter = opt_match.group(1)
                    opt_text = opt_match.group(2).strip()
                    options_found[opt_letter] = opt_text
                i += 1

            # Expect ANSWER: X
            answer = None
            if i < len(lines) and re.match(r'^ANSWER:\s*([A-D])', lines[i], re.IGNORECASE):
                ans_match = re.match(r'^ANSWER:\s*([A-D])', lines[i], re.IGNORECASE)
                if ans_match:
                    answer = ans_match.group(1).upper()
                i += 1
            else:
                errors.append(f"Missing ANSWER line for question: '{question_text[:40]}...'")

            if len(options_found) >= 2 and answer and answer in options_found:
                parsed_questions.append({
                    "question_text": question_text,
                    "option_a": options_found.get("A", "N/A"),
                    "option_b": options_found.get("B", "N/A"),
                    "option_c": options_found.get("C", "N/A"),
                    "option_d": options_found.get("D", "N/A"),
                    "correct_answer": answer
                })
            else:
                if len(options_found) < 2:
                    errors.append(f"Insufficient options for question: '{question_text[:40]}...'")

        return parsed_questions, errors

    @staticmethod
    def import_aiken_questions(
        subject_id: str,
        raw_text: str,
        default_difficulty: str = "Medium",
        default_marks: float = 1.0,
        topic: str = "General",
        teacher_id: str = None
    ) -> Dict[str, Any]:
        parsed, errors = AikenParser.parse_aiken_string(raw_text)

        conn = get_db_connection()
        cursor = conn.cursor()
        now = datetime.utcnow().isoformat()
        imported_ids = []

        for q in parsed:
            qid = str(uuid.uuid4())
            cursor.execute("""
                INSERT INTO questions (
                    id, subject_id, teacher_id, question_text,
                    option_a, option_b, option_c, option_d,
                    correct_answer, marks, difficulty, topic,
                    explanation, is_active, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
            """, (
                qid, subject_id, teacher_id, q["question_text"],
                q["option_a"], q["option_b"], q["option_c"], q["option_d"],
                q["correct_answer"], default_marks, default_difficulty,
                topic, "Imported via Aiken batch ingestion.", now, now
            ))
            imported_ids.append(qid)

        conn.commit()

        return {
            "total_parsed": len(parsed),
            "successful_imports": len(imported_ids),
            "failed_count": len(errors),
            "errors": errors,
            "imported_question_ids": imported_ids
        }
