"""
ExamHub - 3-Parameter Logistic (3PL) IRT Engine
Implements Lord's 3PL model incorporating pseudo-guessing parameter (c)
for multiple-choice assessments.
"""

import math
from typing import List, Dict, Any, Tuple, Optional

class ThreeParameterLogisticModel:
    """
    3-Parameter Logistic (3PL) IRT Model:
    P(theta) = c + (1 - c) / (1 + exp(-1.702 * a * (theta - b)))
    c: lower asymptote (pseudo-guessing probability, typically 1 / num_options = 0.25)
    """

    SCALING_D = 1.702

    @staticmethod
    def probability(theta: float, a: float, b: float, c: float = 0.25) -> float:
        d = ThreeParameterLogisticModel.SCALING_D
        exponent = -d * a * (theta - b)
        exponent_clamped = max(-35.0, min(35.0, exponent))
        logistic_part = 1.0 / (1.0 + math.exp(exponent_clamped))
        return c + (1.0 - c) * logistic_part

    @staticmethod
    def item_information(theta: float, a: float, b: float, c: float = 0.25) -> float:
        """
        Fisher Information for 3PL:
        I(theta) = D^2 * a^2 * ((P(theta) - c)^2 / (1 - c)^2) * ((1 - P(theta)) / P(theta))
        """
        p = ThreeParameterLogisticModel.probability(theta, a, b, c)
        if p <= c or p >= 1.0:
            return 0.0

        d = ThreeParameterLogisticModel.SCALING_D
        term1 = (d ** 2) * (a ** 2)
        term2 = ((p - c) ** 2) / ((1.0 - c) ** 2)
        term3 = (1.0 - p) / p

        return term1 * term2 * term3

    @staticmethod
    def calculate_test_information(
        thetas: List[float],
        items: List[Tuple[float, float, float]]  # List of (a, b, c) tuples
    ) -> List[Dict[str, float]]:
        result = []
        for th in thetas:
            info_sum = sum(ThreeParameterLogisticModel.item_information(th, a, b, c) for a, b, c in items)
            sem = 1.0 / math.sqrt(info_sum) if info_sum > 0.001 else 9.99
            result.append({
                "theta": round(th, 2),
                "test_information": round(info_sum, 3),
                "sem": round(sem, 3)
            })
        return result
