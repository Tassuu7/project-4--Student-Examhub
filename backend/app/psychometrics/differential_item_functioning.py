"""
ExamHub - Differential Item Functioning (DIF) Bias Detection
Implements Mantel-Haenszel statistic to detect item bias against demographic or cohort subgroups
controlling for total candidate ability level.
"""

from typing import List, Dict, Any, Tuple
import math

class DifferentialItemFunctioningEngine:
    """Detects unfair item bias across reference and focal groups."""

    @staticmethod
    def mantel_haenszel_dif(
        reference_responses: List[Dict[str, Any]],
        focal_responses: List[Dict[str, Any]],
        strata_count: int = 5
    ) -> Dict[str, Any]:
        """
        Calculates Mantel-Haenszel common odds-ratio (alpha_MH) and Delta-DIF.
        reference_responses: [{'is_correct': 1, 'total_score': 85.0}, ...]
        focal_responses: [{'is_correct': 1, 'total_score': 82.0}, ...]
        """
        all_scores = [r["total_score"] for r in reference_responses + focal_responses]
        if not all_scores:
            return {}

        min_score = min(all_scores)
        max_score = max(all_scores)
        score_range = max(1.0, max_score - min_score)
        stratum_width = score_range / strata_count

        sum_num = 0.0
        sum_den = 0.0

        for s in range(strata_count):
            lower = min_score + s * stratum_width
            upper = min_score + (s + 1) * stratum_width

            # 2x2 contingency table for stratum s:
            # Reference: A (correct), B (wrong)
            # Focal:     C (correct), D (wrong)
            ref_stratum = [r for r in reference_responses if lower <= r["total_score"] <= upper]
            focal_stratum = [r for r in focal_responses if lower <= r["total_score"] <= upper]

            a = sum(1 for r in ref_stratum if r["is_correct"] == 1)
            b = len(ref_stratum) - a
            c = sum(1 for r in focal_stratum if r["is_correct"] == 1)
            d = len(focal_stratum) - c
            n_stratum = a + b + c + d

            if n_stratum > 0 and (b * c) > 0:
                sum_num += (a * d) / n_stratum
                sum_den += (b * c) / n_stratum

        if sum_den <= 0.0001:
            alpha_mh = 1.0
        else:
            alpha_mh = sum_num / sum_den

        # ETS Delta DIF metric: Delta_MH = -2.35 * ln(alpha_MH)
        if alpha_mh > 0:
            delta_mh = -2.35 * math.log(alpha_mh)
        else:
            delta_mh = 0.0

        abs_delta = abs(delta_mh)
        if abs_delta < 1.0:
            ets_category = "Class A (Negligible DIF - Unbiased)"
        elif abs_delta < 1.5:
            ets_category = "Class B (Moderate DIF - Review Recommended)"
        else:
            ets_category = "Class C (Severe DIF - Flagged for Removal)"

        return {
            "reference_candidates": len(reference_responses),
            "focal_candidates": len(focal_responses),
            "mantel_haenszel_odds_ratio": round(alpha_mh, 3),
            "ets_delta_dif": round(delta_mh, 3),
            "classification": ets_category,
            "favors": "Reference Group" if delta_mh < -1.0 else ("Focal Group" if delta_mh > 1.0 else "Neutral")
        }
