"""
ExamHub Ordering and Sequencing Engine
Grades ordered items using Kendall's Tau and Spearman's Rank Correlation for partial credit.
"""

from typing import List
from backend.app.question_engines.schemas import (
    OrderingGradingRequest,
    OrderingGradingResponse,
)


class OrderingEngine:
    """
    Computes permutation agreement distance for items ordered by a candidate.
    """

    @classmethod
    def calculate_kendalls_tau(cls, cand_order: List[str], correct_order: List[str]) -> float:
        """
        Kendall's Tau-a:
        Tau = (Concordant Pairs - Discordant Pairs) / Total Pairs
        """
        if len(cand_order) != len(correct_order) or len(cand_order) < 2:
            return 1.0 if cand_order == correct_order else 0.0

        item_rank_target = {item: idx for idx, item in enumerate(correct_order)}
        ranks = [item_rank_target[item] for item in cand_order if item in item_rank_target]

        n = len(ranks)
        if n < 2:
            return 1.0

        concordant = 0
        discordant = 0

        for i in range(n):
            for j in range(i + 1, n):
                if ranks[i] < ranks[j]:
                    concordant += 1
                elif ranks[i] > ranks[j]:
                    discordant += 1

        total_pairs = n * (n - 1) / 2
        tau = (concordant - discordant) / total_pairs
        return round(tau, 3)

    @classmethod
    def calculate_spearman_rho(cls, cand_order: List[str], correct_order: List[str]) -> float:
        """
        Spearman's Rank Correlation:
        Rho = 1 - (6 * sum(d_i^2)) / (n * (n^2 - 1))
        """
        n = len(cand_order)
        if n != len(correct_order) or n < 2:
            return 1.0 if cand_order == correct_order else 0.0

        target_map = {item: i for i, item in enumerate(correct_order)}
        sum_d_sq = 0.0

        for cand_idx, item in enumerate(cand_order):
            target_idx = target_map.get(item, cand_idx)
            diff = cand_idx - target_idx
            sum_d_sq += (diff * diff)

        rho = 1.0 - (6.0 * sum_d_sq) / (n * (n * n - 1))
        return round(rho, 3)

    @classmethod
    def evaluate(cls, req: OrderingGradingRequest) -> OrderingGradingResponse:
        is_perf = (req.candidate_order == req.correct_order)
        tau = cls.calculate_kendalls_tau(req.candidate_order, req.correct_order)
        rho = cls.calculate_spearman_rho(req.candidate_order, req.correct_order)

        if is_perf:
            partial_score = 1.0
        elif req.scoring_method == "kendalls_tau":
            # Scale tau from [-1, 1] to [0, 1]
            partial_score = max(0.0, (tau + 1.0) / 2.0)
        else:
            partial_score = max(0.0, (rho + 1.0) / 2.0)

        return OrderingGradingResponse(
            is_perfect=is_perf,
            partial_score=round(partial_score, 3),
            kendall_tau=tau,
            spearman_rho=rho
        )
