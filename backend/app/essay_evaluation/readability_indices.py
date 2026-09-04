"""
ExamHub - Psycholinguistic & Readability Metric Engine
Computes standard academic readability benchmarks: Flesch-Kincaid,
Gunning Fog, Coleman-Liau, and Automated Readability Index.
"""

import re
import math
from typing import Dict, Any

class ReadabilityEngine:
    """Calculates reading complexity and educational grade levels of written essays."""

    @staticmethod
    def count_syllables_in_word(word: str) -> int:
        """Heuristic rule-based syllable counter for English text."""
        w = word.lower().strip()
        if len(w) <= 3:
            return 1

        w = re.sub(r'(?:[^laeiouy]|ed|es|e)$', '', w)
        w = re.sub(r'^y', '', w)
        syllables = len(re.findall(r'[aeiouy]{1,2}', w))
        return max(1, syllables)

    @staticmethod
    def analyze_text_corpus(text: str) -> Dict[str, Any]:
        cleaned = text.strip()
        if not cleaned:
            return {
                "word_count": 0, "sentence_count": 0, "syllable_count": 0,
                "flesch_reading_ease": 0.0, "flesch_kincaid_grade": 0.0,
                "gunning_fog": 0.0, "coleman_liau": 0.0, "automated_readability_index": 0.0
            }

        sentences = [s.strip() for s in re.split(r'[.!?]+', cleaned) if s.strip()]
        sentence_count = max(1, len(sentences))

        words = re.findall(r'\b[a-zA-Z]+\b', cleaned)
        word_count = max(1, len(words))

        total_syllables = sum(ReadabilityEngine.count_syllables_in_word(w) for w in words)
        complex_words = sum(1 for w in words if ReadabilityEngine.count_syllables_in_word(w) >= 3)
        total_letters = sum(len(w) for w in words)

        # Flesch Reading Ease: 206.835 - 1.015 * (words/sentences) - 84.6 * (syllables/words)
        asl = word_count / sentence_count
        asw = total_syllables / word_count
        fre = 206.835 - (1.015 * asl) - (84.6 * asw)
        fre = max(0.0, min(100.0, fre))

        # Flesch-Kincaid Grade Level: 0.39 * (words/sentences) + 11.8 * (syllables/words) - 15.59
        fkg = (0.39 * asl) + (11.8 * asw) - 15.59
        fkg = max(0.0, min(20.0, fkg))

        # Gunning Fog Index: 0.4 * ((words/sentences) + 100 * (complex_words/words))
        pct_complex = (complex_words / word_count) * 100.0
        gfi = 0.4 * (asl + pct_complex)

        # Coleman-Liau: 0.0588 * L - 0.296 * S - 15.8
        # L = avg letters per 100 words, S = avg sentences per 100 words
        l_param = (total_letters / word_count) * 100.0
        s_param = (sentence_count / word_count) * 100.0
        cli = (0.0588 * l_param) - (0.296 * s_param) - 15.8
        cli = max(0.0, min(20.0, cli))

        # ARI (Automated Readability Index): 4.71 * (letters/words) + 0.5 * (words/sentences) - 21.43
        ari = (4.71 * (total_letters / word_count)) + (0.5 * asl) - 21.43
        ari = max(0.0, min(20.0, ari))

        return {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "syllable_count": total_syllables,
            "complex_words_count": complex_words,
            "flesch_reading_ease": round(fre, 1),
            "flesch_kincaid_grade": round(fkg, 1),
            "gunning_fog": round(gfi, 1),
            "coleman_liau": round(cli, 1),
            "automated_readability_index": round(ari, 1)
        }
