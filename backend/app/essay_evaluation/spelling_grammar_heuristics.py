"""
ExamHub - Rule-Based Grammar, Syntax, and Punctuation Validator
Analyzes written essay mechanics: sentence capitalization, punctuation balance,
run-on sentences, and repeated word errors.
"""

import re
from typing import List, Dict, Any

class WritingMechanicsValidator:
    """Detects mechanical writing errors without external heavy models."""

    @staticmethod
    def audit_mechanics(text: str) -> Dict[str, Any]:
        errors = []
        raw = text.strip()
        if not raw:
            return {"error_count": 0, "errors": [], "mechanics_score": 100}

        # 1. Check capitalized sentence beginnings
        sentences = [s.strip() for s in re.split(r'[.!?]+', raw) if s.strip()]
        for s in sentences:
            if s and not s[0].isupper() and not s[0].isdigit():
                errors.append(f"Uncapitalized sentence start: '{s[:25]}...'")

        # 2. Check repeated words: "the the", "is is"
        repeated = re.findall(r'\b([a-zA-Z]+)\s+\1\b', raw, re.IGNORECASE)
        for w in repeated:
            errors.append(f"Duplicated consecutive word: '{w} {w}'")

        # 3. Check excessively long run-on sentences (> 45 words without punctuation)
        for s in sentences:
            w_count = len(re.findall(r'\b\w+\b', s))
            if w_count > 45:
                errors.append(f"Run-on sentence detected ({w_count} words): '{s[:35]}...'")

        # 4. Balanced parentheses and quotation marks
        open_parens = raw.count('(')
        close_parens = raw.count(')')
        if open_parens != close_parens:
            errors.append(f"Unbalanced parentheses ({open_parens} open vs {close_parens} close)")

        quotes = raw.count('"')
        if quotes % 2 != 0:
            errors.append("Unclosed quotation mark detected")

        # Deduct score: 100 base - 5 per error
        mechanics_score = max(0, 100 - (len(errors) * 5))

        return {
            "total_sentences": len(sentences),
            "error_count": len(errors),
            "mechanics_score": mechanics_score,
            "errors": errors[:8]  # Top 8 errors
        }
