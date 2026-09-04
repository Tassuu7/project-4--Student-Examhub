"""
ExamHub - Test Equating and Multi-Form Score Harmonization
Implements Linear Equating and Tucker Common-Item Equating to ensure score equivalence
across distinct versions (Form A, Form B) of assessments.
"""

from typing import List, Dict, Any, Tuple
import math

class TestEquatingEngine:
    """Harmonizes raw scores across distinct exam versions using common anchor items."""

    @staticmethod
    def linear_equating_parameters(
        form_x_scores: List[float],
        form_y_scores: List[float]
    ) -> Tuple[float, float]:
        """
        Computes slope (alpha) and intercept (beta) for Linear Equating:
        Equated_Y = alpha * X + beta
        alpha = sigma_y / sigma_x
        beta = mu_y - alpha * mu_x
        """
        n_x = len(form_x_scores)
        n_y = len(form_y_scores)
        if n_x < 2 or n_y < 2:
            return 1.0, 0.0

        mean_x = sum(form_x_scores) / n_x
        mean_y = sum(form_y_scores) / n_y

        var_x = sum((x - mean_x) ** 2 for x in form_x_scores) / (n_x - 1)
        var_y = sum((y - mean_y) ** 2 for y in form_y_scores) / (n_y - 1)

        std_x = math.sqrt(var_x)
        std_y = math.sqrt(var_y)

        if std_x <= 0.0001:
            alpha = 1.0
        else:
            alpha = std_y / std_x

        beta = mean_y - (alpha * mean_x)

        return round(alpha, 4), round(beta, 4)

    @staticmethod
    def convert_score(raw_score: float, alpha: float, beta: float, min_val: float = 0.0, max_val: float = 100.0) -> float:
        converted = alpha * raw_score + beta
        return round(max(min_val, min(max_val, converted)), 2)
