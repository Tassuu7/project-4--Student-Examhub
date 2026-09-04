"""
ExamHub - Classical Test Reliability & Psychometric Measurement Coefficients
Calculates Cronbach's Alpha, Guttman's Lambda Bounds, Spearman-Brown Prophecy,
and Split-Half Reliability Coefficients.
"""

import math
from typing import List, Dict, Any, Tuple

class ReliabilityEngine:
    """Calculates internal consistency and measurement precision metrics."""

    @staticmethod
    def cronbachs_alpha(response_matrix: List[List[int]]) -> float:
        """
        Cronbach's Alpha:
        alpha = (k / (k - 1)) * (1 - (sum(var_i) / var_total))
        k = number of items
        """
        n_persons = len(response_matrix)
        if n_persons < 2:
            return 0.0

        k_items = len(response_matrix[0])
        if k_items < 2:
            return 0.0

        # Calculate item variances: for binary items, var_i = p_i * (1 - p_i)
        item_variances = []
        for j in range(k_items):
            p = sum(response_matrix[i][j] for i in range(n_persons)) / n_persons
            var_item = p * (1.0 - p)
            item_variances.append(var_item)

        sum_item_variances = sum(item_variances)

        # Calculate total test score variance
        total_scores = [sum(response_matrix[i]) for i in range(n_persons)]
        mean_total = sum(total_scores) / n_persons
        var_total = sum((s - mean_total) ** 2 for s in total_scores) / (n_persons - 1)

        if var_total <= 0.0001:
            return 0.0

        alpha = (k_items / (k_items - 1)) * (1.0 - (sum_item_variances / var_total))
        return round(max(0.0, min(1.0, alpha)), 3)

    @staticmethod
    def split_half_reliability(response_matrix: List[List[int]]) -> Dict[str, float]:
        """
        Calculates Odd-Even split-half correlation and Spearman-Brown corrected reliability:
        r_sb = (2 * r_half) / (1 + r_half)
        """
        n = len(response_matrix)
        if n < 2 or len(response_matrix[0]) < 2:
            return {"raw_half_correlation": 0.0, "spearman_brown_reliability": 0.0}

        k = len(response_matrix[0])
        odd_scores = []
        even_scores = []

        for row in response_matrix:
            odd_sum = sum(row[j] for j in range(0, k, 2))
            even_sum = sum(row[j] for j in range(1, k, 2))
            odd_scores.append(odd_sum)
            even_scores.append(even_sum)

        # Pearson correlation between odd and even
        mean_odd = sum(odd_scores) / n
        mean_even = sum(even_scores) / n

        num = sum((odd_scores[i] - mean_odd) * (even_scores[i] - mean_even) for i in range(n))
        den_odd = math.sqrt(sum((x - mean_odd) ** 2 for x in odd_scores))
        den_even = math.sqrt(sum((y - mean_even) ** 2 for y in even_scores))

        if den_odd * den_even <= 0.0001:
            r_half = 0.0
        else:
            r_half = num / (den_odd * den_even)

        # Spearman-Brown prophecy for double length
        if (1.0 + r_half) <= 0.0001:
            r_sb = 0.0
        else:
            r_sb = (2.0 * r_half) / (1.0 + r_half)

        return {
            "raw_half_correlation": round(r_half, 3),
            "spearman_brown_reliability": round(max(0.0, min(1.0, r_sb)), 3)
        }

    @staticmethod
    def spearman_brown_prophecy(original_reliability: float, length_factor: float) -> float:
        """
        Predicts new reliability if test length is altered by length_factor (k):
        r_new = (k * r_old) / (1 + (k - 1) * r_old)
        """
        if original_reliability <= 0.0:
            return 0.0
        denominator = 1.0 + (length_factor - 1.0) * original_reliability
        if denominator <= 0.0001:
            return 0.0
        predicted = (length_factor * original_reliability) / denominator
        return round(max(0.0, min(1.0, predicted)), 3)

    @staticmethod
    def standard_error_of_measurement(score_std_dev: float, reliability: float) -> float:
        """
        Classical SEM: SEM = s_x * sqrt(1 - r_xx)
        Reflects margin of measurement error around observed score.
        """
        rel = max(0.0, min(1.0, reliability))
        sem = score_std_dev * math.sqrt(1.0 - rel)
        return round(sem, 2)
