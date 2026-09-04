"""
ExamHub - Cohort Comparison and Hypothesis Testing
Performs statistical hypothesis testing between two student cohorts or exam versions
using Welch's two-sample t-test, Cohen's d effect sizes, and Z-score distributions.
"""

import math
from typing import Dict, Any, List, Optional
from backend.app.analytics.schemas import CohortComparisonResult
from backend.app.analytics.repository import AnalyticsRepository
from backend.app.core.exceptions import ValidationException

class CohortComparisonEngine:
    """Calculates statistical comparative metrics between examination cohorts."""

    @staticmethod
    def compare_cohorts(exam_id_a: str, exam_id_b: str) -> CohortComparisonResult:
        meta_a = AnalyticsRepository.get_exam_metadata(exam_id_a)
        meta_b = AnalyticsRepository.get_exam_metadata(exam_id_b)

        if not meta_a or not meta_b:
            raise ValidationException("Both examination cohorts must exist in the database.")

        scores_a_records = AnalyticsRepository.get_exam_student_scores(exam_id_a)
        scores_b_records = AnalyticsRepository.get_exam_student_scores(exam_id_b)

        scores_a = [float(r["percentage"]) for r in scores_a_records]
        scores_b = [float(r["percentage"]) for r in scores_b_records]

        n1 = len(scores_a)
        n2 = len(scores_b)

        if n1 < 2 or n2 < 2:
            return CohortComparisonResult(
                cohort_a_name=meta_a["name"],
                cohort_b_name=meta_b["name"],
                cohort_a_size=n1,
                cohort_b_size=n2,
                cohort_a_mean=round(sum(scores_a)/n1, 2) if n1 > 0 else 0.0,
                cohort_b_mean=round(sum(scores_b)/n2, 2) if n2 > 0 else 0.0,
                mean_difference=0.0,
                effect_size_cohens_d=0.0,
                t_statistic=0.0,
                p_value=1.0,
                is_statistically_significant=False,
                summary="Insufficient cohort size (minimum 2 candidates per group required for statistical inference)."
            )

        mean_a = sum(scores_a) / n1
        mean_b = sum(scores_b) / n2
        diff = mean_a - mean_b

        var_a = sum((x - mean_a) ** 2 for x in scores_a) / (n1 - 1)
        var_b = sum((x - mean_b) ** 2 for x in scores_b) / (n2 - 1)

        # Pooled Standard Deviation for Cohen's d
        s_pooled = math.sqrt(((n1 - 1) * var_a + (n2 - 1) * var_b) / (n1 + n2 - 2))
        cohens_d = (diff / s_pooled) if s_pooled > 0.0001 else 0.0

        # Welch's t-statistic (unequal variances)
        se_diff = math.sqrt((var_a / n1) + (var_b / n2))
        t_stat = (diff / se_diff) if se_diff > 0.0001 else 0.0

        # Approximate p-value using normal distribution survival function
        # Z-approximation: p = 2 * (1 - Phi(|t|))
        # Standard normal CDF approximation (Abramowitz and Stegun)
        abs_t = abs(t_stat)
        b0 = 0.2316419
        b1 = 0.319381530
        b2 = -0.356563782
        b3 = 1.781477937
        b4 = -1.821255978
        b5 = 1.330274429
        t_val = 1.0 / (1.0 + b0 * abs_t)
        phi_t = (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * abs_t * abs_t)
        norm_cdf = 1.0 - phi_t * (b1*t_val + b2*(t_val**2) + b3*(t_val**3) + b4*(t_val**4) + b5*(t_val**5))
        p_val = max(0.0001, min(1.0, 2.0 * (1.0 - norm_cdf)))

        is_sig = p_val < 0.05

        # Verbal interpretation
        if abs(cohens_d) >= 0.8:
            effect_label = "Large effect size"
        elif abs(cohens_d) >= 0.5:
            effect_label = "Moderate effect size"
        elif abs(cohens_d) >= 0.2:
            effect_label = "Small effect size"
        else:
            effect_label = "Negligible effect size"

        summary = (
            f"{meta_a['name']} (Mean: {mean_a:.1f}%) vs {meta_b['name']} (Mean: {mean_b:.1f}%). "
            f"Difference is {abs(diff):.1f}% ({effect_label}, d={cohens_d:.2f}). "
            f"{'The difference is statistically significant (p < 0.05).' if is_sig else 'The difference is not statistically significant (p >= 0.05).'}"
        )

        return CohortComparisonResult(
            cohort_a_name=meta_a["name"],
            cohort_b_name=meta_b["name"],
            cohort_a_size=n1,
            cohort_b_size=n2,
            cohort_a_mean=round(mean_a, 2),
            cohort_b_mean=round(mean_b, 2),
            mean_difference=round(diff, 2),
            effect_size_cohens_d=round(cohens_d, 3),
            t_statistic=round(t_stat, 3),
            p_value=round(p_val, 4),
            is_statistically_significant=is_sig,
            summary=summary
        )
