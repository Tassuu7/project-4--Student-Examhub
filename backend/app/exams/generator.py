"""
ExamHub - Automated Exam Generator from Question Bank
"""

import random
from typing import List, Dict, Any, Optional
from backend.app.questions.repository import QuestionRepository

class ExamGenerator:
    @staticmethod
    def generate_questions(
        subject_id: str,
        easy_count: int = 0,
        medium_count: int = 0,
        hard_count: int = 0,
        topic: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Samples questions matching subject, difficulty targets, and optional topic.
        """
        questions, _ = QuestionRepository.list_questions(
            subject_id=subject_id,
            topic=topic,
            limit=500
        )

        by_diff: Dict[str, List[Dict[str, Any]]] = {
            "Easy": [],
            "Medium": [],
            "Hard": []
        }

        for q in questions:
            diff = q.get("difficulty", "Medium")
            if diff in by_diff:
                by_diff[diff].append(q)

        selected = []

        # Sample Easy
        if easy_count > 0:
            pool = by_diff["Easy"]
            random.shuffle(pool)
            selected.extend(pool[:easy_count])

        # Sample Medium
        if medium_count > 0:
            pool = by_diff["Medium"]
            random.shuffle(pool)
            selected.extend(pool[:medium_count])

        # Sample Hard
        if hard_count > 0:
            pool = by_diff["Hard"]
            random.shuffle(pool)
            selected.extend(pool[:hard_count])

        # If not enough specific difficulty questions, backfill from remaining
        target_total = easy_count + medium_count + hard_count
        if target_total > 0 and len(selected) < target_total:
            chosen_ids = {q["id"] for q in selected}
            remaining = [q for q in questions if q["id"] not in chosen_ids]
            random.shuffle(remaining)
            needed = target_total - len(selected)
            selected.extend(remaining[:needed])

        return selected
