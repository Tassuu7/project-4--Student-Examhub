"""
ExamHub - Negative Marking & Guesswork Penalty Engine
Applies configurable penalty deductions for incorrect responses to deter random guessing.
Formula: Marks = Correct * PositiveMark - Incorrect * (Fraction * PositiveMark)
"""

from typing import List, Dict, Any, Tuple

class NegativeMarkingEngine:
    """Calculates standardized penalty deductions for incorrect exam submissions."""

    @staticmethod
    def calculate_penalized_score(
        answers: List[Dict[str, Any]],
        penalty_fraction: float = 0.25,
        penalize_unanswered: bool = False,
        allow_negative_total: bool = False
    ) -> Tuple[float, float, float, Dict[str, Any]]:
        """
        Computes (final_score, gross_earned, total_penalties, summary_stats).
        """
        gross_marks = 0.0
        penalties = 0.0
        correct_count = 0
        wrong_count = 0
        unanswered_count = 0

        for ans in answers:
            allocated = float(ans.get("marks_allocated", 1.0))
            is_correct = ans.get("is_correct") == 1
            selected = ans.get("selected_option")

            if selected is None:
                unanswered_count += 1
                if penalize_unanswered:
                    penalties += allocated * penalty_fraction
            elif is_correct:
                correct_count += 1
                gross_marks += allocated
            else:
                wrong_count += 1
                penalties += allocated * penalty_fraction

        net_score = gross_marks - penalties
        if not allow_negative_total:
            net_score = max(0.0, net_score)

        summary = {
            "correct_count": correct_count,
            "wrong_count": wrong_count,
            "unanswered_count": unanswered_count,
            "penalty_fraction": penalty_fraction,
            "gross_score": round(gross_marks, 2),
            "penalty_deducted": round(penalties, 2),
            "net_score": round(net_score, 2)
        }

        return round(net_score, 2), round(gross_marks, 2), round(penalties, 2), summary
