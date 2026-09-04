"""
ExamHub - Automated Evaluation and Grading Engine
"""

from typing import Dict, Any, List, Tuple
from backend.app.core.constants import EvaluationResult

class ExamEvaluator:
    @staticmethod
    def calculate_grade(percentage: float) -> str:
        if percentage >= 90.0:
            return "A+"
        elif percentage >= 80.0:
            return "A"
        elif percentage >= 70.0:
            return "B"
        elif percentage >= 60.0:
            return "C"
        elif percentage >= 50.0:
            return "D"
        elif percentage >= 40.0:
            return "E"
        else:
            return "F"

    @classmethod
    def evaluate_attempt(
        cls,
        exam: Dict[str, Any],
        questions: List[Dict[str, Any]],
        answers_by_qid: Dict[str, Dict[str, Any]]
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Evaluates student responses against answer keys.
        Returns:
            (summary_stats, detailed_evaluations_list)
        """
        total_questions = len(questions)
        correct_count = 0
        wrong_count = 0
        unanswered_count = 0
        total_marks = 0.0
        obtained_marks = 0.0
        details = []

        passing_percentage = float(exam.get("passing_percentage", 40.0))

        for q in questions:
            qid = q["question_id"]
            allocated_marks = float(q.get("marks_allocated", 1.0))
            total_marks += allocated_marks

            ans_record = answers_by_qid.get(qid)
            selected = ans_record.get("selected_option") if ans_record else None
            correct = q.get("correct_answer", "").strip().upper()

            is_correct = False
            q_obtained = 0.0

            if not selected:
                unanswered_count += 1
            elif selected.strip().upper() == correct:
                correct_count += 1
                is_correct = True
                q_obtained = allocated_marks
                obtained_marks += allocated_marks
            else:
                wrong_count += 1

            details.append({
                "question_id": qid,
                "order_index": q.get("order_index", 0),
                "question_text": q["question_text"],
                "option_a": q["option_a"],
                "option_b": q["option_b"],
                "option_c": q["option_c"],
                "option_d": q["option_d"],
                "selected_option": selected,
                "correct_answer": correct,
                "is_correct": is_correct,
                "marks_obtained": q_obtained,
                "max_marks": allocated_marks,
                "explanation": q.get("explanation"),
                "topic": q.get("topic")
            })

        percentage = round((obtained_marks / total_marks * 100.0) if total_marks > 0 else 0.0, 2)
        grade = cls.calculate_grade(percentage)
        pass_fail = EvaluationResult.PASS.value if percentage >= passing_percentage else EvaluationResult.FAIL.value

        summary = {
            "total_questions": total_questions,
            "correct_count": correct_count,
            "wrong_count": wrong_count,
            "unanswered_count": unanswered_count,
            "total_marks": total_marks,
            "obtained_marks": obtained_marks,
            "percentage": percentage,
            "grade": grade,
            "pass_fail": pass_fail
        }

        return summary, details
