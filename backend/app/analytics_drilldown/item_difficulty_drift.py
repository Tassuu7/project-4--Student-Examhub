"""
ExamHub Longitudinal Item Parameter Drift (IPD) Engine
Detects temporal shifts in question difficulty over multiple testing administrations (flagging question compromise).
"""

from typing import List, Dict
from backend.app.analytics_drilldown.schemas import (
    TermDifficultyRecord,
    ItemParameterDrift,
)


class ItemDriftAnalyzer:
    """
    Evaluates whether an item's difficulty changes significantly over time.
    A drop in difficulty b of > 0.40 logits with high P-value often indicates question leak/compromise.
    """

    DRIFT_THRESHOLD_LOGITS: float = 0.35

    @classmethod
    def evaluate_item_drift(cls, item_id: str, history: List[TermDifficultyRecord]) -> ItemParameterDrift:
        if len(history) < 2:
            return ItemParameterDrift(
                item_id=item_id,
                term_history=history,
                drift_delta_b=0.0,
                is_drift_significant=False,
                drift_direction="STABLE"
            )

        # Compare first term against most recent term
        first_b = history[0].difficulty_b
        latest_b = history[-1].difficulty_b
        delta_b = latest_b - first_b

        is_significant = abs(delta_b) >= cls.DRIFT_THRESHOLD_LOGITS

        if not is_significant:
            direction = "STABLE"
        elif delta_b < 0:
            # Drop in b means item has gotten easier
            direction = "EASIER (Potential Question Leakage)"
        else:
            # Rise in b means item has gotten harder
            direction = "HARDER (Curricular Misalignment)"

        return ItemParameterDrift(
            item_id=item_id,
            term_history=history,
            drift_delta_b=round(delta_b, 3),
            is_drift_significant=is_significant,
            drift_direction=direction
        )
