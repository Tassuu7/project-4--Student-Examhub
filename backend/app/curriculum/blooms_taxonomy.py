"""
ExamHub - Bloom's Revised Taxonomy Cognitive Classification
Audits exam blueprints to ensure balanced representation across lower-order (LOTS)
and higher-order thinking skills (HOTS).
"""

from typing import List, Dict, Any, Tuple
from collections import Counter

class BloomsTaxonomyEngine:
    """Classifies cognitive complexity and measures blueprint balance."""

    LEVELS = [
        "Remembering",
        "Understanding",
        "Applying",
        "Analyzing",
        "Evaluating",
        "Creating"
    ]

    ACTION_VERBS = {
        "Remembering": {"define", "identify", "list", "name", "recall", "recognize", "state", "match"},
        "Understanding": {"classify", "describe", "explain", "summarize", "paraphrase", "interpret", "exemplify"},
        "Applying": {"apply", "calculate", "demonstrate", "implement", "solve", "execute", "use"},
        "Analyzing": {"differentiate", "distinguish", "examine", "compare", "contrast", "deconstruct", "outline"},
        "Evaluating": {"appraise", "critique", "defend", "judge", "evaluate", "justify", "rate"},
        "Creating": {"construct", "design", "formulate", "synthesize", "generate", "invent", "plan"}
    }

    @staticmethod
    def infer_blooms_level(question_text: str) -> str:
        words = question_text.lower().split()
        first_few = words[:5]

        for level, verbs in BloomsTaxonomyEngine.ACTION_VERBS.items():
            for v in verbs:
                if v in first_few or v in words:
                    return level

        return "Understanding"  # Default baseline

    @staticmethod
    def audit_exam_cognitive_balance(questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        total = len(questions)
        if total == 0:
            return {"lots_percentage": 0.0, "hots_percentage": 0.0, "is_balanced": False}

        counts = Counter()
        for q in questions:
            level = q.get("blooms_level") or BloomsTaxonomyEngine.infer_blooms_level(q.get("question_text", ""))
            counts[level] += 1

        lots_count = counts["Remembering"] + counts["Understanding"]
        hots_count = counts["Applying"] + counts["Analyzing"] + counts["Evaluating"] + counts["Creating"]

        lots_pct = round((lots_count / total) * 100.0, 1)
        hots_pct = round((hots_count / total) * 100.0, 1)

        # Ideal university exam target: 40-50% LOTS, 50-60% HOTS
        is_balanced = (30.0 <= lots_pct <= 60.0)

        breakdown = [
            {"level": lvl, "count": counts[lvl], "percentage": round((counts[lvl] / total) * 100.0, 1)}
            for lvl in BloomsTaxonomyEngine.LEVELS
        ]

        return {
            "total_questions": total,
            "lots_count": lots_count,
            "lots_percentage": lots_pct,
            "hots_count": hots_count,
            "hots_percentage": hots_pct,
            "is_cognitively_balanced": is_balanced,
            "levels_breakdown": breakdown,
            "recommendation": "Optimal cognitive distribution" if is_balanced else "Incorporate more Higher-Order Thinking Skills (HOTS) questions"
        }
