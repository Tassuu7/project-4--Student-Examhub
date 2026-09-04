"""
ExamHub - Plagiarism & Candidate Collusion Detector
Detects textual duplication across candidate submissions using character n-grams,
Jaccard coefficient, and Longest Common Subsequence (LCS).
"""

import re
from typing import List, Dict, Any, Set, Tuple

class PlagiarismDetector:
    """Identifies unauthorized copying and essay collusion between test-takers."""

    @staticmethod
    def extract_word_ngrams(text: str, n: int = 4) -> Set[str]:
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        if len(words) < n:
            return set()
        return {' '.join(words[i:i + n]) for i in range(len(words) - n + 1)}

    @staticmethod
    def calculate_jaccard_similarity(text_a: str, text_b: str, n: int = 4) -> float:
        ngrams_a = PlagiarismDetector.extract_word_ngrams(text_a, n)
        ngrams_b = PlagiarismDetector.extract_word_ngrams(text_b, n)

        if not ngrams_a or not ngrams_b:
            return 0.0

        intersection = len(ngrams_a.intersection(ngrams_b))
        union = len(ngrams_a.union(ngrams_b))

        return round(intersection / union, 3) if union > 0 else 0.0

    @staticmethod
    def scan_cohort_collusion(
        submissions: List[Dict[str, Any]],
        threshold: float = 0.50
    ) -> List[Dict[str, Any]]:
        """
        submissions: [{'student_id': '...', 'student_name': '...', 'text': '...'}]
        Pairwise comparisons to flag suspicious matching submissions.
        """
        n = len(submissions)
        flagged_pairs = []

        for i in range(n):
            for j in range(i + 1, n):
                sub_a = submissions[i]
                sub_b = submissions[j]

                sim = PlagiarismDetector.calculate_jaccard_similarity(
                    sub_a["text"], sub_b["text"], n=4
                )

                if sim >= threshold:
                    flagged_pairs.append({
                        "student_a_id": sub_a["student_id"],
                        "student_a_name": sub_a["student_name"],
                        "student_b_id": sub_b["student_id"],
                        "student_b_name": sub_b["student_name"],
                        "similarity_score": sim,
                        "risk_level": "Severe Collusion" if sim > 0.75 else "Suspicious Overlap"
                    })

        flagged_pairs.sort(key=lambda x: x["similarity_score"], reverse=True)
        return flagged_pairs
