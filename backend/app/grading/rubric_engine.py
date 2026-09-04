"""
ExamHub - Rubric Evaluation & Partial Credit Computation
Evaluates multi-dimensional criteria grids with weighted scoring and floor bounds.
"""

from typing import List, Dict, Any, Optional

class RubricEngine:
    """Evaluates qualitative student performance against defined rubric matrices."""

    @staticmethod
    def evaluate_submission(
        criteria_definitions: List[Dict[str, Any]],
        ratings_assigned: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Computes composite score:
        Sum(rating * weight) / Sum(max_score * weight) * total_points
        """
        total_obtained = 0.0
        total_possible = 0.0
        breakdown = []

        for crit in criteria_definitions:
            cid = crit["id"]
            weight = float(crit.get("weight", 1.0))
            max_score = float(crit.get("max_score", 10.0))
            awarded = float(ratings_assigned.get(cid, 0.0))
            awarded = max(0.0, min(max_score, awarded))

            weighted_obtained = awarded * weight
            weighted_max = max_score * weight

            total_obtained += weighted_obtained
            total_possible += weighted_max

            breakdown.append({
                "criterion_id": cid,
                "name": crit.get("name", "Criterion"),
                "raw_score": awarded,
                "max_score": max_score,
                "weight": weight,
                "weighted_score": round(weighted_obtained, 2)
            })

        final_percentage = (total_obtained / total_possible * 100.0) if total_possible > 0 else 0.0

        return {
            "total_obtained": round(total_obtained, 2),
            "total_possible": round(total_possible, 2),
            "percentage": round(final_percentage, 2),
            "breakdown": breakdown
        }
