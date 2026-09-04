"""
ExamHub - Computerized Adaptive Testing (CAT) Engine
Selects optimal assessment items dynamically using Maximum Fisher Information (MFI),
enforces content balancing constraints, and monitors convergence criteria.
"""

from typing import List, Dict, Any, Tuple, Optional
import math
from backend.app.psychometrics.two_parameter_logistic import TwoParameterLogisticModel

class ComputerizedAdaptiveTestingEngine:
    """Dynamic item selection and stopping rule engine for personalized adaptive exams."""

    @staticmethod
    def select_next_item_mfi(
        current_theta: float,
        available_items: List[Dict[str, Any]],
        administered_item_ids: List[str],
        topic_target_proportions: Optional[Dict[str, float]] = None,
        topic_administered_counts: Optional[Dict[str, int]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Selects item from available pool that maximizes Fisher Information at current_theta,
        incorporating topic content balancing weights.
        """
        unseen_items = [it for it in available_items if it["id"] not in administered_item_ids]
        if not unseen_items:
            return None

        best_item = None
        highest_utility = -1.0

        for item in unseen_items:
            a = float(item.get("discrimination_a", 1.0))
            b = float(item.get("difficulty_b", 0.0))
            topic = item.get("topic", "General")

            # Calculate Fisher information
            info = TwoParameterLogisticModel.item_information(current_theta, a, b)

            # Content balancing multiplier
            if topic_target_proportions and topic_administered_counts:
                target_pct = topic_target_proportions.get(topic, 0.25)
                current_count = topic_administered_counts.get(topic, 0)
                total_admin = sum(topic_administered_counts.values()) or 1
                current_pct = current_count / total_admin

                # Boost weight if topic is underrepresented
                if current_pct < target_pct:
                    content_boost = 1.3
                else:
                    content_boost = 0.8
            else:
                content_boost = 1.0

            utility = info * content_boost

            if utility > highest_utility:
                highest_utility = utility
                best_item = item

        return best_item

    @staticmethod
    def check_stopping_criteria(
        current_sem: float,
        items_administered_count: int,
        target_sem: float = 0.30,
        min_items: int = 10,
        max_items: int = 35
    ) -> Tuple[bool, str]:
        """
        Evaluates whether adaptive examination should conclude.
        Returns (should_stop, reason).
        """
        if items_administered_count < min_items:
            return False, "Below minimum test length"

        if items_administered_count >= max_items:
            return True, "Maximum item limit reached"

        if current_sem <= target_sem:
            return True, f"Measurement precision attained (SEM: {current_sem} <= {target_sem})"

        return False, "Continuing adaptive item selection"
