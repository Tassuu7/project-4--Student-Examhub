"""
ExamHub Score Scaling Engine
Transforms raw test marks into Z-scores, T-scores, Stanine (Standard Nine), and standardized scaled scores.
"""

import math
from typing import List, Tuple
from backend.app.analytics_drilldown.schemas import StandardizedScoreRecord


class ScoreScalingEngine:
    """
    Standard psychometric normalizations for high-stakes test reporting.
    """

    @classmethod
    def normal_cdf(cls, z: float) -> float:
        """Standard normal cumulative distribution approximation."""
        return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))

    @classmethod
    def z_to_stanine(cls, z: float) -> int:
        """
        Maps Z-score into Stanine bands (1 to 9):
        Stanine 1: Z < -1.75
        Stanine 2: -1.75 <= Z < -1.25
        Stanine 3: -1.25 <= Z < -0.75
        Stanine 4: -0.75 <= Z < -0.25
        Stanine 5: -0.25 <= Z < +0.25
        Stanine 6: +0.25 <= Z < +0.75
        Stanine 7: +0.75 <= Z < +1.25
        Stanine 8: +1.25 <= Z < +1.75
        Stanine 9: Z >= +1.75
        """
        if z < -1.75:
            return 1
        elif z < -1.25:
            return 2
        elif z < -0.75:
            return 3
        elif z < -0.25:
            return 4
        elif z < 0.25:
            return 5
        elif z < 0.75:
            return 6
        elif z < 1.25:
            return 7
        elif z < 1.75:
            return 8
        else:
            return 9

    @classmethod
    def standardize_cohort_scores(
        cls,
        candidate_scores: List[Tuple[str, float, float]]  # (candidate_id, raw_score, max_possible)
    ) -> List[StandardizedScoreRecord]:
        """
        Computes Z, T, Stanine, and 500-scale scores across a cohort.
        """
        if not candidate_scores:
            return []

        raws = [raw for _, raw, _ in candidate_scores]
        n = len(raws)
        mean_score = sum(raws) / n
        var = sum((x - mean_score) ** 2 for x in raws) / (n if n > 1 else 1)
        sd = math.sqrt(var) if var > 1e-6 else 1.0

        records: List[StandardizedScoreRecord] = []
        for cid, raw, max_pts in candidate_scores:
            pct = (raw / max_pts * 100.0) if max_pts > 0 else 0.0
            z = (raw - mean_score) / sd
            t = 50.0 + (10.0 * z)
            stanine = cls.z_to_stanine(z)
            percentile = round(cls.normal_cdf(z) * 100.0, 1)

            # Scaled score: mean 300, sd 50, bounded [100, 500]
            scaled = int(round(300.0 + (50.0 * z)))
            scaled = max(100, min(500, scaled))

            rec = StandardizedScoreRecord(
                candidate_id=cid,
                raw_score=round(raw, 2),
                percentage=round(pct, 2),
                z_score=round(z, 3),
                t_score=round(t, 2),
                stanine=stanine,
                percentile=percentile,
                scaled_score_500=scaled
            )
            records.append(rec)

        return records
