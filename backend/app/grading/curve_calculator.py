"""
ExamHub - Statistical Grade Curve Transformation Engine
Calculates score adjustments via Linear Offset, Square Root Scaling,
and Standardized Z-Score Normalization (Bell Curve).
"""

import math
from typing import List, Dict, Any, Tuple

class CurveCalculator:
    """Mathematical transformations for academic grade adjustments."""

    @staticmethod
    def apply_square_root_curve(scores: List[float], total_marks: float) -> List[float]:
        """
        Classic scaling: Curved% = sqrt(Raw%) * 10
        Transforms score proportionally while preserving relative rank.
        """
        curved = []
        for s in scores:
            pct = (s / total_marks * 100.0) if total_marks > 0 else 0.0
            pct = max(0.0, min(100.0, pct))
            new_pct = math.sqrt(pct) * 10.0
            new_score = (new_pct / 100.0) * total_marks
            curved.append(round(new_score, 2))
        return curved

    @staticmethod
    def apply_linear_offset(scores: List[float], total_marks: float, target_mean: float) -> List[float]:
        """Shifts all scores by a constant delta so the cohort reaches target_mean."""
        n = len(scores)
        if n == 0:
            return []
        current_mean = sum(scores) / n
        current_mean_pct = (current_mean / total_marks) * 100.0
        delta_pct = target_mean - current_mean_pct
        delta_marks = (delta_pct / 100.0) * total_marks

        curved = []
        for s in scores:
            new_s = max(0.0, min(total_marks, s + delta_marks))
            curved.append(round(new_s, 2))
        return curved

    @staticmethod
    def apply_bell_curve(
        scores: List[float],
        total_marks: float,
        target_mean_pct: float = 75.0,
        target_std_pct: float = 12.0
    ) -> List[float]:
        """Standardizes scores via Z-score and remaps to target normal distribution."""
        n = len(scores)
        if n < 2:
            return scores

        mean = sum(scores) / n
        var = sum((x - mean) ** 2 for x in scores) / (n - 1)
        std_dev = math.sqrt(var)

        if std_dev < 0.0001:
            return scores

        curved = []
        for s in scores:
            z_score = (s - mean) / std_dev
            curved_pct = target_mean_pct + (z_score * target_std_pct)
            curved_pct = max(0.0, min(100.0, curved_pct))
            curved_marks = (curved_pct / 100.0) * total_marks
            curved.append(round(curved_marks, 2))
        return curved
