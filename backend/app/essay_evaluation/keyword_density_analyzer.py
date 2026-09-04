"""
ExamHub - Lexical Diversity & Curriculum Keyword Density Analyzer
Evaluates vocabulary range (Type-Token Ratio, Hapax Legomena),
and checks presence of required subject matter terminology.
"""

import re
from typing import List, Dict, Any, Set
from collections import Counter

class LexicalAnalyzer:
    """Calculates vocabulary richness and required topic coverage."""

    STOPWORDS: Set[str] = {
        'the', 'is', 'at', 'which', 'on', 'and', 'a', 'an', 'in', 'to', 'of',
        'for', 'with', 'as', 'by', 'that', 'this', 'it', 'from', 'be', 'are',
        'was', 'were', 'or', 'but', 'not', 'have', 'has', 'had', 'they', 'we'
    }

    @staticmethod
    def analyze_lexical_diversity(text: str) -> Dict[str, Any]:
        raw_tokens = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        total_tokens = len(raw_tokens)
        if total_tokens == 0:
            return {"type_token_ratio": 0.0, "unique_words": 0, "hapax_legomena": 0}

        counts = Counter(raw_tokens)
        unique_types = len(counts)
        ttr = unique_types / total_tokens

        # Hapax legomena: words occurring exactly once (sign of varied vocabulary)
        hapax = sum(1 for w, c in counts.items() if c == 1)

        # Content words (non-stopwords)
        content_words = [w for w in raw_tokens if w not in LexicalAnalyzer.STOPWORDS]
        lexical_density = len(content_words) / total_tokens

        return {
            "total_tokens": total_tokens,
            "unique_types": unique_types,
            "type_token_ratio": round(ttr, 3),
            "hapax_legomena_count": hapax,
            "lexical_density": round(lexical_density, 3),
            "top_frequent_words": counts.most_common(5)
        }

    @staticmethod
    def check_required_keywords(text: str, target_keywords: List[str]) -> Dict[str, Any]:
        tokens_set = set(re.findall(r'\b[a-zA-Z]+\b', text.lower()))
        matched = []
        missing = []

        for kw in target_keywords:
            kw_clean = kw.lower().strip()
            if kw_clean in tokens_set:
                matched.append(kw)
            else:
                missing.append(kw)

        coverage_pct = (len(matched) / len(target_keywords) * 100.0) if target_keywords else 100.0

        return {
            "total_required": len(target_keywords),
            "matched_count": len(matched),
            "missing_count": len(missing),
            "coverage_percentage": round(coverage_pct, 1),
            "matched_keywords": matched,
            "missing_keywords": missing
        }
