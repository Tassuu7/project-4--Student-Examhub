"""
ExamHub - Grading Application Service
Orchestrates curve scaling, negative marking evaluation, and rubric scoring.
"""

from typing import Dict, Any, List, Optional
from backend.app.grading.curve_calculator import CurveCalculator
from backend.app.grading.moderation import GradeModerationManager
from backend.app.grading.schemas import GradeCurveResult
from backend.app.database.connection import get_db_connection
from backend.app.core.exceptions import NotFoundException

class GradingService:
    """Service layer managing exam-wide score transformations and regrading."""

    @staticmethod
    def apply_curve(exam_id: str, method: str, target_mean: Optional[float] = None) -> GradeCurveResult:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT total_marks FROM exams WHERE id = ?", (exam_id,))
        exam_row = cursor.fetchone()
        if not exam_row:
            raise NotFoundException(f"Exam '{exam_id}' not found.")

        total_marks = float(exam_row[0])
        cursor.execute("SELECT id, attempt_id, obtained_marks, percentage FROM results WHERE exam_id = ?", (exam_id,))
        results = [dict(r) for r in cursor.fetchall()]

        if not results:
            return GradeCurveResult(
                exam_id=exam_id, method=method, original_mean=0.0,
                curved_mean=0.0, adjusted_scores_count=0, score_deltas=[]
            )

        original_scores = [float(r["obtained_marks"]) for r in results]
        orig_mean = sum(original_scores) / len(original_scores)

        if method == "square_root":
            curved = CurveCalculator.apply_square_root_curve(original_scores, total_marks)
        elif method == "linear_offset":
            target = target_mean or 75.0
            curved = CurveCalculator.apply_linear_offset(original_scores, total_marks, target)
        elif method == "bell_curve":
            curved = CurveCalculator.apply_bell_curve(original_scores, total_marks)
        else:
            curved = original_scores

        deltas = []
        for idx, r in enumerate(results):
            new_val = curved[idx]
            old_val = original_scores[idx]
            new_pct = (new_val / total_marks * 100.0) if total_marks > 0 else 0.0

            cursor.execute("""
                UPDATE results
                SET obtained_marks = ?, percentage = ?
                WHERE id = ?
            """, (new_val, round(new_pct, 2), r["id"]))

            deltas.append({
                "attempt_id": r["attempt_id"],
                "old_score": old_val,
                "curved_score": new_val,
                "delta": round(new_val - old_val, 2)
            })

        conn.commit()
        curved_mean = sum(curved) / len(curved) if curved else 0.0

        return GradeCurveResult(
            exam_id=exam_id,
            method=method,
            original_mean=round(orig_mean, 2),
            curved_mean=round(curved_mean, 2),
            adjusted_scores_count=len(deltas),
            score_deltas=deltas
        )

    @staticmethod
    def adjust_single_score(payload: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        return GradeModerationManager.adjust_student_score(
            attempt_id=payload["attempt_id"],
            question_id=payload["question_id"],
            new_marks=float(payload["new_marks"]),
            reason=payload["adjustment_reason"],
            moderator_user_id=user_id
        )
