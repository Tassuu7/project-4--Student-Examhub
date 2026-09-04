"""
ExamHub Essay Evaluation - Coherence & Discourse Flow Engine
Analyzes discourse markers, sentence transition logic, topical continuity, and rhetorical structure.
"""

import re
from typing import List, Dict, Tuple, Set
from pydantic import BaseModel, Field


class DiscourseAnalysisReport(BaseModel):
    paragraph_count: int
    sentence_count: int
    mean_sentence_length_words: float
    transition_words_count: int
    transition_density_per_100_words: float
    paragraph_cohesion_score: float  # 0.0 to 10.0
    rhetorical_balance_score: float  # 0.0 to 10.0
    detected_transition_types: Dict[str, int]
    recommendations: List[str]


class CoherenceFlowEvaluator:
    """
    Evaluates argumentative and descriptive essay structure for automated scoring.
    """

    TRANSITION_CATEGORIES = {
        "addition": ["furthermore", "moreover", "in addition", "additionally", "besides", "also"],
        "contrast": ["however", "nevertheless", "on the contrary", "conversely", "despite", "although", "whereas"],
        "causation": ["therefore", "consequently", "as a result", "thus", "hence", "accordingly"],
        "exemplification": ["for example", "for instance", "to illustrate", "specifically", "namely"],
        "conclusion": ["in conclusion", "to summarize", "ultimately", "in summary", "overall"]
    }

    @classmethod
    def split_paragraphs(cls, text: str) -> List[str]:
        return [p.strip() for p in text.split("\n\n") if p.strip()]

    @classmethod
    def split_sentences(cls, text: str) -> List[str]:
        sentences = re.split(r"[.!?]+", text)
        return [s.strip() for s in sentences if len(s.strip().split()) > 2]

    @classmethod
    def analyze_flow(cls, essay_text: str) -> DiscourseAnalysisReport:
        paragraphs = cls.split_paragraphs(essay_text)
        sentences = cls.split_sentences(essay_text)
        words = re.findall(r"\b[a-zA-Z]+\b", essay_text.lower())
        total_words = len(words)

        if total_words == 0:
            return DiscourseAnalysisReport(
                paragraph_count=0,
                sentence_count=0,
                mean_sentence_length_words=0.0,
                transition_words_count=0,
                transition_density_per_100_words=0.0,
                paragraph_cohesion_score=0.0,
                rhetorical_balance_score=0.0,
                detected_transition_types={},
                recommendations=["Essay contains no readable text."]
            )

        mean_sent_len = len(words) / max(1, len(sentences))

        # Count transition markers
        lower_text = essay_text.lower()
        transition_counts: Dict[str, int] = {}
        total_transitions = 0

        for cat, markers in cls.TRANSITION_CATEGORIES.items():
            count = 0
            for m in markers:
                count += len(re.findall(r"\b" + re.escape(m) + r"\b", lower_text))
            transition_counts[cat] = count
            total_transitions += count

        transition_density = (total_transitions / total_words) * 100.0

        # Paragraph cohesion: check if paragraphs link to previous paragraph's vocabulary
        cohesion_scores = []
        if len(paragraphs) > 1:
            for i in range(1, len(paragraphs)):
                prev_words = set(re.findall(r"\b[a-zA-Z]{4,}\b", paragraphs[i - 1].lower()))
                cur_words = set(re.findall(r"\b[a-zA-Z]{4,}\b", paragraphs[i].lower()))
                overlap = len(prev_words.intersection(cur_words))
                cohesion_scores.append(min(1.0, overlap / 4.0))
            avg_cohesion = sum(cohesion_scores) / len(cohesion_scores) * 10.0
        else:
            avg_cohesion = 6.0

        # Rhetorical balance score
        used_categories_count = sum(1 for c, cnt in transition_counts.items() if cnt > 0)
        rhetorical_balance = min(10.0, (used_categories_count / len(cls.TRANSITION_CATEGORIES)) * 8.0 + (min(total_transitions, 6) / 6.0) * 2.0)

        # Recommendations
        recs = []
        if len(paragraphs) < 3:
            recs.append("Essay structure lacks formal multi-paragraph division (introduction, body arguments, conclusion).")
        if transition_counts.get("contrast", 0) == 0:
            recs.append("Consider incorporating counterarguments using contrast transitions ('however', 'nevertheless') to strengthen argumentation.")
        if transition_counts.get("causation", 0) == 0:
            recs.append("Strengthen logical causality by employing connecting markers ('therefore', 'consequently').")
        if not recs:
            recs.append("Excellent rhetorical structure and fluent discourse connectivity across paragraphs.")

        return DiscourseAnalysisReport(
            paragraph_count=len(paragraphs),
            sentence_count=len(sentences),
            mean_sentence_length_words=round(mean_sent_len, 1),
            transition_words_count=total_transitions,
            transition_density_per_100_words=round(transition_density, 2),
            paragraph_cohesion_score=round(avg_cohesion, 1),
            rhetorical_balance_score=round(rhetorical_balance, 1),
            detected_transition_types=transition_counts,
            recommendations=recs
        )
