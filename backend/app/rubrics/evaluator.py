"""
ExamHub Rubric Evaluation and Inter-Rater Reliability Engine
Computes Cohen's Kappa for pairwise marker agreement and Fleiss' Kappa for multi-marker consensus.
"""

import math
from typing import List, Dict, Any, Tuple, Optional
from backend.app.rubrics.schemas import (
    RubricDefinition,
    CriterionScoreInput,
    EvaluationRecord,
    InterRaterReliabilityResult,
)


class RubricEvaluator:
    """
    Evaluates submissions against structured rubrics and assesses grading consistency
    across human markers using standard psychometric agreement statistics.
    """

    @classmethod
    def calculate_score(
        cls,
        rubric: RubricDefinition,
        scores: List[CriterionScoreInput]
    ) -> Tuple[float, float, Dict[str, float], Dict[str, str]]:
        """
        Calculate weighted score and percentage from criterion scores.
        Returns: (total_score, percentage, criterion_scores_dict, criterion_levels_dict)
        """
        criterion_map = {c.criterion_id: c for c in rubric.criteria}
        total_score = 0.0
        max_possible = 0.0
        scores_dict = {}
        levels_dict = {}

        for sc in scores:
            crit = criterion_map.get(sc.criterion_id)
            if not crit:
                continue

            # Find matching level
            level_obj = next((l for l in crit.levels if l.level_id == sc.selected_level_id), None)
            level_points = level_obj.points if level_obj else 0.0

            points = sc.adjusted_score if sc.adjusted_score is not None else level_points
            weighted_points = points * crit.weight
            total_score += weighted_points

            max_crit_pts = max([l.points for l in crit.levels], default=0.0) * crit.weight
            max_possible += max_crit_pts

            scores_dict[sc.criterion_id] = round(points, 2)
            levels_dict[sc.criterion_id] = sc.selected_level_id

        pct = (total_score / max_possible * 100.0) if max_possible > 0 else 0.0
        return round(total_score, 2), round(pct, 2), scores_dict, levels_dict

    @classmethod
    def calculate_cohens_kappa(cls, rater1_cats: List[int], rater2_cats: List[int], num_cats: int) -> float:
        """
        Calculate Cohen's Kappa for two raters assigning items to categorical bands.
        """
        n = len(rater1_cats)
        if n == 0 or len(rater2_cats) != n:
            return 0.0

        # Build confusion matrix
        matrix = [[0 for _ in range(num_cats)] for _ in range(num_cats)]
        for r1, r2 in zip(rater1_cats, rater2_cats):
            if 0 <= r1 < num_cats and 0 <= r2 < num_cats:
                matrix[r1][r2] += 1

        # Observed agreement P_o
        po = sum(matrix[i][i] for i in range(num_cats)) / n

        # Expected chance agreement P_e
        row_totals = [sum(matrix[i]) for i in range(num_cats)]
        col_totals = [sum(matrix[i][j] for i in range(num_cats)) for j in range(num_cats)]

        pe = sum((row_totals[k] * col_totals[k]) for k in range(num_cats)) / (n * n)

        if abs(1.0 - pe) < 1e-9:
            return 1.0  # Perfect agreement on trivial category

        kappa = (po - pe) / (1.0 - pe)
        return round(max(-1.0, min(1.0, kappa)), 3)

    @classmethod
    def calculate_fleiss_kappa(cls, rating_matrix: List[List[int]]) -> float:
        """
        Calculate Fleiss' Kappa for multiple raters on multiple subjects.
        matrix shape: [N_subjects, K_categories], where matrix[i][j] is count of raters
        who assigned subject i to category j.
        """
        N = len(rating_matrix)
        if N == 0:
            return 0.0
        k = len(rating_matrix[0])
        n = sum(rating_matrix[0])  # raters per subject
        if n <= 1:
            return 0.0

        # Calculate P_i for each subject
        P_i = []
        for i in range(N):
            sum_sq = sum(rating_matrix[i][j] * rating_matrix[i][j] for j in range(k))
            p_val = (sum_sq - n) / (n * (n - 1))
            P_i.append(p_val)
        P_bar = sum(P_i) / N

        # Calculate p_j for each category
        p_j = []
        for j in range(k):
            col_sum = sum(rating_matrix[i][j] for i in range(N))
            p_j.append(col_sum / (N * n))

        P_e_bar = sum(pj * pj for pj in p_j)

        if abs(1.0 - P_e_bar) < 1e-9:
            return 1.0

        kappa = (P_bar - P_e_bar) / (1.0 - P_e_bar)
        return round(max(-1.0, min(1.0, kappa)), 3)

    @classmethod
    def interpret_kappa(cls, kappa: float) -> str:
        """
        Standard Landis & Koch (1977) interpretation of Kappa coefficients.
        """
        if kappa < 0.0:
            return "Poor Agreement (Worse than chance)"
        elif kappa <= 0.20:
            return "Slight Agreement"
        elif kappa <= 0.40:
            return "Fair Agreement"
        elif kappa <= 0.60:
            return "Moderate Agreement"
        elif kappa <= 0.80:
            return "Substantial Agreement"
        else:
            return "Almost Perfect Agreement"
