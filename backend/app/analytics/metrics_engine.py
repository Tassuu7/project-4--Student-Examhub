"""
ExamHub - Psychometrics and Statistical Engine
Implements Classical Test Theory (CTT), Item Response Theory (IRT) proxies,
Kelley's 27% discrimination rule, and descriptive distributional statistics.
"""

import math
from typing import List, Dict, Any, Tuple, Optional
from collections import Counter
from backend.app.analytics.schemas import (
    ScoreSummary, PassFailMetrics, GradeBucket,
    QuestionItemMetric, DecileDistribution
)

class MetricsEngine:
    """Mathematical and statistical computing engine for examination metrics."""

    @staticmethod
    def calculate_score_summary(scores: List[float], total_marks: float) -> ScoreSummary:
        n = len(scores)
        if n == 0:
            return ScoreSummary(
                total_candidates=0, evaluated_candidates=0, mean_score=0.0,
                median_score=0.0, mode_score=None, standard_deviation=0.0,
                variance=0.0, minimum_score=0.0, maximum_score=0.0,
                range_score=0.0, q1_score=0.0, q3_score=0.0, iqr_score=0.0,
                skewness=0.0, kurtosis=0.0
            )

        sorted_scores = sorted(scores)
        mean_score = sum(sorted_scores) / n

        # Median
        if n % 2 == 1:
            median_score = sorted_scores[n // 2]
        else:
            median_score = (sorted_scores[n // 2 - 1] + sorted_scores[n // 2]) / 2.0

        # Mode
        freq = Counter(sorted_scores)
        max_freq = max(freq.values())
        modes = [k for k, v in freq.items() if v == max_freq]
        mode_score = modes[0] if len(modes) == 1 and max_freq > 1 else None

        # Variance and Standard Deviation
        variance = sum((x - mean_score) ** 2 for x in sorted_scores) / (n if n == 1 else (n - 1))
        std_dev = math.sqrt(variance)

        # Quartiles
        def get_percentile(p: float) -> float:
            k = (n - 1) * p
            f = math.floor(k)
            c = math.ceil(k)
            if f == c:
                return sorted_scores[int(k)]
            d0 = sorted_scores[int(f)] * (c - k)
            d1 = sorted_scores[int(c)] * (k - f)
            return d0 + d1

        q1 = get_percentile(0.25)
        q3 = get_percentile(0.75)
        iqr = q3 - q1

        # Skewness (Fisher-Pearson)
        if n > 2 and std_dev > 0.0001:
            skewness = (n / ((n - 1) * (n - 2))) * sum(((x - mean_score) / std_dev) ** 3 for x in sorted_scores)
        else:
            skewness = 0.0

        # Kurtosis (Excess kurtosis relative to normal distribution)
        if n > 3 and std_dev > 0.0001:
            c1 = (n * (n + 1)) / ((n - 1) * (n - 2) * (n - 3))
            sum_pow4 = sum(((x - mean_score) / std_dev) ** 4 for x in sorted_scores)
            c2 = (3 * ((n - 1) ** 2)) / ((n - 2) * (n - 3))
            kurtosis = c1 * sum_pow4 - c2
        else:
            kurtosis = 0.0

        min_score = sorted_scores[0]
        max_score = sorted_scores[-1]

        return ScoreSummary(
            total_candidates=n,
            evaluated_candidates=n,
            mean_score=round(mean_score, 2),
            median_score=round(median_score, 2),
            mode_score=round(mode_score, 2) if mode_score is not None else None,
            standard_deviation=round(std_dev, 2),
            variance=round(variance, 2),
            minimum_score=round(min_score, 2),
            maximum_score=round(max_score, 2),
            range_score=round(max_score - min_score, 2),
            q1_score=round(q1, 2),
            q3_score=round(q3, 2),
            iqr_score=round(iqr, 2),
            skewness=round(skewness, 2),
            kurtosis=round(kurtosis, 2)
        )

    @staticmethod
    def calculate_pass_fail(scores: List[float], passing_percentage: float, total_marks: float) -> PassFailMetrics:
        n = len(scores)
        threshold_marks = (passing_percentage / 100.0) * total_marks
        if n == 0:
            return PassFailMetrics(
                total_appeared=0, passed_count=0, failed_count=0,
                passing_percentage=passing_percentage, pass_rate=0.0,
                fail_rate=0.0, threshold_marks=threshold_marks
            )

        passed = sum(1 for s in scores if s >= threshold_marks)
        failed = n - passed

        return PassFailMetrics(
            total_appeared=n,
            passed_count=passed,
            failed_count=failed,
            passing_percentage=passing_percentage,
            pass_rate=round((passed / n) * 100.0, 2),
            fail_rate=round((failed / n) * 100.0, 2),
            threshold_marks=round(threshold_marks, 2)
        )

    @staticmethod
    def calculate_grade_distribution(percentages: List[float]) -> List[GradeBucket]:
        total = len(percentages)
        tiers = [
            ("A+", 90.0, 100.0, "#10b981"),
            ("A", 80.0, 89.99, "#059669"),
            ("B+", 70.0, 79.99, "#3b82f6"),
            ("B", 60.0, 69.99, "#2563eb"),
            ("C", 50.0, 59.99, "#f59e0b"),
            ("D", 40.0, 49.99, "#d97706"),
            ("F", 0.0, 39.99, "#ef4444"),
        ]

        buckets = []
        for grade, min_val, max_val, color in tiers:
            count = sum(1 for p in percentages if min_val <= p <= (max_val + (0.01 if grade == "A+" else 0.0)))
            pct = round((count / total * 100.0), 2) if total > 0 else 0.0
            buckets.append(GradeBucket(
                grade=grade,
                count=count,
                percentage=pct,
                min_score=min_val,
                max_score=max_val,
                color_code=color
            ))
        return buckets

    @staticmethod
    def calculate_deciles(scores: List[float], total_marks: float) -> List[DecileDistribution]:
        n = len(scores)
        deciles = []
        for i in range(10):
            lower_pct = i * 10.0
            upper_pct = (i + 1) * 10.0
            lower_score = (lower_pct / 100.0) * total_marks
            upper_score = (upper_pct / 100.0) * total_marks

            if i == 9:
                count = sum(1 for s in scores if lower_score <= s <= total_marks)
            else:
                count = sum(1 for s in scores if lower_score <= s < upper_score)

            pct_cohort = round((count / n * 100.0), 2) if n > 0 else 0.0
            deciles.append(DecileDistribution(
                decile=f"{int(lower_pct)}-{int(upper_pct)}%",
                lower_bound=round(lower_score, 1),
                upper_bound=round(upper_score, 1),
                student_count=count,
                percentage_of_cohort=pct_cohort
            ))
        return deciles

    @staticmethod
    def calculate_item_psychometrics(
        question_id: str,
        question_meta: Dict[str, Any],
        student_records: List[Dict[str, Any]]
    ) -> QuestionItemMetric:
        """
        Computes item facility (P), Kelley's discrimination index (D), and point-biserial correlation (r_pbis).
        student_records contains dicts with:
        {'selected_option': 'A', 'is_correct': 1, 'student_total_score': 85.0}
        """
        n = len(student_records)
        if n == 0:
            return QuestionItemMetric(
                question_id=question_id,
                order_index=question_meta.get("order_index", 1),
                question_text=question_meta.get("question_text", ""),
                difficulty_assigned=question_meta.get("difficulty", "Medium"),
                topic=question_meta.get("topic"),
                marks_allocated=float(question_meta.get("marks_allocated", 1.0)),
                total_attempts=0,
                correct_attempts=0,
                wrong_attempts=0,
                unanswered_attempts=0,
                facility_index=0.0,
                discrimination_index=0.0,
                point_biserial=0.0,
                discrimination_status="Defective",
                option_a_selection_rate=0.0,
                option_b_selection_rate=0.0,
                option_c_selection_rate=0.0,
                option_d_selection_rate=0.0
            )

        correct_count = sum(1 for r in student_records if r.get("is_correct") == 1)
        unanswered_count = sum(1 for r in student_records if r.get("selected_option") is None)
        wrong_count = n - correct_count - unanswered_count

        facility_p = correct_count / n

        # Options breakdown
        opt_a = sum(1 for r in student_records if r.get("selected_option") == "A") / n
        opt_b = sum(1 for r in student_records if r.get("selected_option") == "B") / n
        opt_c = sum(1 for r in student_records if r.get("selected_option") == "C") / n
        opt_d = sum(1 for r in student_records if r.get("selected_option") == "D") / n

        # Kelley's 27% Rule for Item Discrimination
        sorted_by_total = sorted(student_records, key=lambda x: float(x.get("student_total_score", 0.0)))
        kelley_size = max(1, int(math.ceil(0.27 * n)))
        lower_group = sorted_by_total[:kelley_size]
        upper_group = sorted_by_total[-kelley_size:]

        upper_correct = sum(1 for r in upper_group if r.get("is_correct") == 1)
        lower_correct = sum(1 for r in lower_group if r.get("is_correct") == 1)

        p_upper = upper_correct / len(upper_group)
        p_lower = lower_correct / len(lower_group)
        discrimination_d = p_upper - p_lower

        # Status categorization
        if discrimination_d >= 0.40:
            status = "Excellent"
        elif discrimination_d >= 0.30:
            status = "Good"
        elif discrimination_d >= 0.20:
            status = "Marginal"
        elif discrimination_d >= 0.0:
            status = "Poor"
        else:
            status = "Defective"

        # Point-biserial correlation: r_pbis = ((M1 - M0) / Sn) * sqrt(p * q)
        correct_scores = [float(r.get("student_total_score", 0.0)) for r in student_records if r.get("is_correct") == 1]
        wrong_scores = [float(r.get("student_total_score", 0.0)) for r in student_records if r.get("is_correct") != 1]
        all_scores = [float(r.get("student_total_score", 0.0)) for r in student_records]

        if correct_scores and wrong_scores and len(all_scores) > 1:
            mean_1 = sum(correct_scores) / len(correct_scores)
            mean_0 = sum(wrong_scores) / len(wrong_scores)
            mean_all = sum(all_scores) / n
            variance_all = sum((x - mean_all) ** 2 for x in all_scores) / n
            std_all = math.sqrt(variance_all)
            p_val = correct_count / n
            q_val = 1.0 - p_val
            if std_all > 0.0001:
                point_biserial = ((mean_1 - mean_0) / std_all) * math.sqrt(p_val * q_val)
                point_biserial = max(-1.0, min(1.0, point_biserial))
            else:
                point_biserial = 0.0
        else:
            point_biserial = 0.0

        return QuestionItemMetric(
            question_id=question_id,
            order_index=question_meta.get("order_index", 1),
            question_text=question_meta.get("question_text", ""),
            difficulty_assigned=question_meta.get("difficulty", "Medium"),
            topic=question_meta.get("topic"),
            marks_allocated=float(question_meta.get("marks_allocated", 1.0)),
            total_attempts=n,
            correct_attempts=correct_count,
            wrong_attempts=wrong_count,
            unanswered_attempts=unanswered_count,
            facility_index=round(facility_p, 3),
            discrimination_index=round(discrimination_d, 3),
            point_biserial=round(point_biserial, 3),
            discrimination_status=status,
            option_a_selection_rate=round(opt_a, 3),
            option_b_selection_rate=round(opt_b, 3),
            option_c_selection_rate=round(opt_c, 3),
            option_d_selection_rate=round(opt_d, 3)
        )
