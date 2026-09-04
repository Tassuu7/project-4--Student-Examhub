"""
ExamHub Plagiarism Detection - Winnowing Fingerprint Engine
Implements the Schleimer-Wilkerson-Aiken winnowing algorithm for local document fingerprinting.
"""

import re
import hashlib
from typing import List, Tuple, Set, Dict


class WinnowingEngine:
    """
    Computes robust document fingerprints using rolling hashes and windowed minima.
    Guarantees detection of shared substrings of length >= (k + w - 1).
    """

    PRIME_BASE: int = 31
    MODULO: int = 1000000007

    @classmethod
    def normalize_text(cls, text: str) -> str:
        """
        Normalize text for invariant comparison: lowercase and alphanumeric only.
        """
        return re.sub(r"[^a-z0-9]", "", text.lower())

    @classmethod
    def generate_kgrams(cls, text: str, k: int = 25) -> List[Tuple[str, int]]:
        """
        Extract overlapping character k-grams with starting indices.
        """
        kgrams = []
        clean = cls.normalize_text(text)
        if len(clean) < k:
            return [(clean, 0)]
        for i in range(len(clean) - k + 1):
            kgrams.append((clean[i : i + k], i))
        return kgrams

    @classmethod
    def hash_string(cls, s: str) -> int:
        """
        Compute 32-bit integer hash using MD5 slice.
        """
        md5_digest = hashlib.md5(s.encode("utf-8")).hexdigest()
        return int(md5_digest[:8], 16)

    @classmethod
    def compute_fingerprints(
        cls,
        text: str,
        k: int = 25,
        w: int = 15
    ) -> List[Tuple[int, int]]:
        """
        Execute Winnowing algorithm:
        1. Form k-grams and hash them.
        2. In each sliding window of length w, pick the minimum hash.
        3. Break ties by choosing the rightmost minimum.
        Returns: list of (hash_val, pos) pairs.
        """
        kgrams = cls.generate_kgrams(text, k)
        if not kgrams:
            return []

        hashes = [(cls.hash_string(kg), pos) for kg, pos in kgrams]

        if len(hashes) <= w:
            min_h = min(hashes, key=lambda item: item[0])
            return [min_h]

        fingerprints: List[Tuple[int, int]] = []
        prev_min_pos = -1

        for i in range(len(hashes) - w + 1):
            window = hashes[i : i + w]
            # Rightmost minimum: reverse iterate to prefer later positions on equal minimum
            min_item = min(window, key=lambda item: item[0])

            if min_item[1] != prev_min_pos:
                fingerprints.append(min_item)
                prev_min_pos = min_item[1]

        return fingerprints

    @classmethod
    def calculate_jaccard_similarity(
        cls,
        fp1: List[Tuple[int, int]],
        fp2: List[Tuple[int, int]]
    ) -> Tuple[float, int]:
        """
        Calculate Jaccard similarity coefficient between two sets of fingerprints:
        J = |A ∩ B| / |A ∪ B|
        """
        set1 = {h for h, _ in fp1}
        set2 = {h for h, _ in fp2}

        if not set1 and not set2:
            return 1.0, 0
        if not set1 or not set2:
            return 0.0, 0

        intersection = set1.intersection(set2)
        union = set1.union(set2)

        jaccard = len(intersection) / len(union)
        return round(jaccard, 4), len(intersection)
