"""
ExamHub - Discourse Coherence & Argumentative Flow Analyzer
Evaluates transitional linking words, paragraph topic progression,
and rhetorical cohesion in student academic essays.
"""

import re
from typing import List, Dict, Any, Set

class DiscourseCoherenceAnalyzer:
    """Evaluates transitional discourse markers and essay paragraph structure."""

    TRANSITIONAL_MARKERS: Set[str] = {
        'furthermore', 'moreover', 'in addition', 'consequently', 'therefore',
        'however', 'nevertheless', 'nonetheless', 'on the other hand', 'similarly',
        'likewise', 'specifically', 'for instance', 'for example', 'in conclusion',
        'to summarize', 'as a result', 'in contrast', 'ultimately', 'notably'
    }

    @staticmethod
    def analyze_coherence(text: str) -> Dict[str, Any]:
        paragraphs = [p.strip() for p in text.strip().split('\n\n') if p.strip()]
        total_paragraphs = len(paragraphs)

        text_lower = text.lower()
        found_markers = []
        for marker in DiscourseCoherenceAnalyzer.TRANSITIONAL_MARKERS:
            count = len(re.findall(r'\b' + re.escape(marker) + r'\b', text_lower))
            if count > 0:
                found_markers.append({"marker": marker, "count": count})

        total_markers_used = sum(m["count"] for m in found_markers)

        # Structure analysis
        has_intro = total_paragraphs >= 2
        has_conclusion = any('conclusion' in p.lower() or 'summar' in p.lower() for p in paragraphs[-1:])

        if total_markers_used >= 6 and total_paragraphs >= 3:
            rating = "Strong Coherence & Natural Transitions"
        elif total_markers_used >= 3:
            rating = "Adequate Structure & Flow"
        else:
            rating = "Weak Transitional Flow - Choppy Paragraphs"

        return {
            "paragraph_count": total_paragraphs,
            "transitional_markers_count": total_markers_used,
            "distinct_markers_used": len(found_markers),
            "markers_breakdown": found_markers,
            "has_clear_structure": has_intro,
            "has_conclusion_marker": has_conclusion,
            "coherence_rating": rating
        }
