"""
ExamHub Cloze Fill-in-the-Blanks Engine
Grades multi-gap text questions with regex matching and Levenshtein edit distance tolerance.
"""

import re
from typing import Dict, List
from backend.app.question_engines.schemas import (
    ClozeGradingRequest,
    ClozeGradingResponse,
    ClozeGapRule,
)


class ClozeEngine:
    """
    Evaluates candidate text filled into blanks/gaps within passages.
    """

    @classmethod
    def levenshtein_distance(cls, s1: str, s2: str) -> int:
        """Computes minimum single-character edits between s1 and s2."""
        if len(s1) < len(s2):
            return cls.levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    @classmethod
    def grade_gap(cls, candidate_text: str, rule: ClozeGapRule) -> bool:
        """Check if candidate text matches rule requirements."""
        cand = candidate_text.strip()
        if not rule.case_sensitive:
            cand = cand.lower()

        # Check regex if present
        if rule.regex_pattern:
            flags = 0 if rule.case_sensitive else re.IGNORECASE
            if re.fullmatch(rule.regex_pattern, candidate_text.strip(), flags=flags):
                return True

        # Check acceptable answers list
        for target in rule.acceptable_answers:
            tgt = target.strip()
            if not rule.case_sensitive:
                tgt = tgt.lower()

            if rule.allow_typo_distance > 0:
                dist = cls.levenshtein_distance(cand, tgt)
                if dist <= rule.allow_typo_distance:
                    return True
            else:
                if cand == tgt:
                    return True

        return False

    @classmethod
    def evaluate(cls, req: ClozeGradingRequest) -> ClozeGradingResponse:
        results: Dict[int, bool] = {}
        feedback: Dict[int, str] = {}
        correct_count = 0

        for rule in req.gap_rules:
            idx = rule.gap_index
            cand_ans = req.candidate_answers.get(idx, "")
            is_right = cls.grade_gap(cand_ans, rule)
            results[idx] = is_right

            if is_right:
                correct_count += 1
                feedback[idx] = "Correct"
            else:
                feedback[idx] = f"Incorrect. Target answers: {', '.join(rule.acceptable_answers[:3])}"

        total = len(req.gap_rules)
        pct = (correct_count / total * 100.0) if total > 0 else 0.0

        return ClozeGradingResponse(
            total_gaps=total,
            correct_gaps=correct_count,
            score_percentage=round(pct, 2),
            gap_results=results,
            feedback_per_gap=feedback
        )
