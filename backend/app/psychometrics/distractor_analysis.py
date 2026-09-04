"""
ExamHub - Multiple-Choice Distractor Functioning Analysis
Evaluates option plausibility, non-functioning distractors (< 5% selection),
and positive distractor discrimination anomalies.
"""

from typing import List, Dict, Any, Tuple
import math

class DistractorAnalysisEngine:
    """Evaluates multiple-choice option efficacy across ability strata."""

    @staticmethod
    def analyze_item_options(
        responses: List[Dict[str, Any]],
        correct_option: str
    ) -> Dict[str, Any]:
        """
        responses: List of dicts with 'selected_option' ('A','B','C','D',None) and 'student_score' (float).
        """
        n = len(responses)
        if n == 0:
            return {}

        # Divide into Upper 33%, Middle 34%, and Lower 33% groups
        sorted_resp = sorted(responses, key=lambda x: float(x.get("student_score", 0.0)))
        tier_size = max(1, n // 3)

        lower_group = sorted_resp[:tier_size]
        upper_group = sorted_resp[-tier_size:]
        middle_group = sorted_resp[tier_size:-tier_size]

        options = ['A', 'B', 'C', 'D']
        option_diagnostics = []
        non_functioning_count = 0

        for opt in options:
            is_key = (opt == correct_option)

            total_chosen = sum(1 for r in responses if r.get("selected_option") == opt)
            upper_chosen = sum(1 for r in upper_group if r.get("selected_option") == opt)
            middle_chosen = sum(1 for r in middle_group if r.get("selected_option") == opt)
            lower_chosen = sum(1 for r in lower_group if r.get("selected_option") == opt)

            p_total = total_chosen / n
            p_upper = upper_chosen / len(upper_group)
            p_lower = lower_chosen / len(lower_group)

            discrimination = p_upper - p_lower

            # Diagnostic checks
            # For correct key: discrimination should be POSITIVE (> 0.20)
            # For distractors: discrimination should be NEGATIVE (chosen more by lower group)
            # Non-functioning distractor if chosen by less than 5% of students
            if is_key:
                status = "Correct Key"
                flag = "Needs Review: Negative Key Discrimination" if discrimination < 0 else "Normal"
            else:
                if p_total < 0.05:
                    status = "Non-Functioning Distractor"
                    flag = "Unattractive Option (<5% selection)"
                    non_functioning_count += 1
                elif discrimination > 0.05:
                    status = "Misleading Distractor"
                    flag = "Ambiguous: Top students chosen distractor more than lower students"
                else:
                    status = "Effective Distractor"
                    flag = "Normal"

            option_diagnostics.append({
                "option": opt,
                "is_correct_key": is_key,
                "total_selection_rate": round(p_total, 3),
                "upper_group_rate": round(p_upper, 3),
                "middle_group_rate": round(middle_chosen / len(middle_group) if middle_group else 0.0, 3),
                "lower_group_rate": round(p_lower, 3),
                "option_discrimination": round(discrimination, 3),
                "functioning_status": status,
                "diagnostic_flag": flag
            })

        return {
            "total_candidates": n,
            "correct_key": correct_option,
            "non_functioning_distractor_count": non_functioning_count,
            "item_health": "Healthy Item" if non_functioning_count == 0 else f"{non_functioning_count} Distractor(s) require replacement",
            "options": option_diagnostics
        }
