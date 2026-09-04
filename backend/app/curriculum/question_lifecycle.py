"""
ExamHub - Item Banking Quality Assurance & Peer Review Lifecycle
Governs multi-stage approval workflows for question bank items.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

class QuestionLifecycleManager:
    """Manages formal peer-review status transitions for assessment questions."""

    VALID_STATUSES = {
        "draft", "in_review", "revision_requested", "approved", "staged_for_exam", "archived"
    }

    TRANSITION_RULES = {
        "draft": {"in_review", "archived"},
        "in_review": {"approved", "revision_requested", "draft"},
        "revision_requested": {"in_review", "draft"},
        "approved": {"staged_for_exam", "archived"},
        "staged_for_exam": {"approved", "archived"},
        "archived": {"draft"}
    }

    @staticmethod
    def validate_transition(current_status: str, new_status: str) -> bool:
        allowed = QuestionLifecycleManager.TRANSITION_RULES.get(current_status, set())
        return new_status in allowed

    @staticmethod
    def evaluate_quality_checklist(
        question_text: str,
        options: List[str],
        has_explanation: bool,
        topic_assigned: bool
    ) -> Dict[str, Any]:
        """Quality audit before permitting transition to approved status."""
        checks = []

        # Check 1: Stem length
        has_sufficient_stem = len(question_text.split()) >= 6
        checks.append({"rule": "Clear question stem (>= 6 words)", "passed": has_sufficient_stem})

        # Check 2: Plausible options
        valid_options = all(len(opt.strip()) > 0 for opt in options)
        checks.append({"rule": "Non-empty distractors", "passed": valid_options})

        # Check 3: Explanation provided
        checks.append({"rule": "Pedagogical explanation attached", "passed": has_explanation})

        # Check 4: Topic tagged
        checks.append({"rule": "Curriculum topic tagged", "passed": topic_assigned})

        all_passed = all(c["passed"] for c in checks)

        return {
            "is_approval_ready": all_passed,
            "checklist": checks,
            "quality_score": round((sum(1 for c in checks if c["passed"]) / len(checks)) * 100.0, 1)
        }
