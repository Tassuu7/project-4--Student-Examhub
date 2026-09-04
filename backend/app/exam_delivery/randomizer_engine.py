"""
ExamHub Exam Item Randomizer Engine
Performs deterministic question shuffling and option permutations seeded by candidate & exam keys.
"""

import hashlib
import random
from typing import List, Dict, Any
from backend.app.exam_delivery.schemas import ShuffledQuestionItem


class RandomizerEngine:
    """
    Generates deterministic individualized exam layouts for each candidate
    to eliminate adjacent screen eavesdropping in exam testing halls.
    """

    @classmethod
    def get_seed(cls, candidate_id: str, exam_id: str) -> int:
        combined = f"{candidate_id}:{exam_id}".encode("utf-8")
        digest = hashlib.sha256(combined).hexdigest()
        return int(digest[:8], 16)

    @classmethod
    def generate_candidate_package(
        cls,
        candidate_id: str,
        exam_id: str,
        raw_questions: List[Dict[str, Any]]
    ) -> List[ShuffledQuestionItem]:
        """
        Shuffles questions and internal options deterministically using seed.
        """
        seed = cls.get_seed(candidate_id, exam_id)
        rng = random.Random(seed)

        # Shuffle questions list copy
        shuffled_q_list = list(raw_questions)
        rng.shuffle(shuffled_q_list)

        output_items: List[ShuffledQuestionItem] = []

        for idx, q in enumerate(shuffled_q_list):
            raw_options = q.get("options", [])
            # Create indexed option objects
            indexed_opts = [
                {"original_index": opt_idx, "text": opt_text}
                for opt_idx, opt_text in enumerate(raw_options)
            ]
            rng.shuffle(indexed_opts)

            # Assign keys A, B, C, D...
            option_letters = ["A", "B", "C", "D", "E", "F"]
            final_opts = []
            for opt_pos, opt_dict in enumerate(indexed_opts):
                letter = option_letters[opt_pos] if opt_pos < len(option_letters) else f"Opt{opt_pos}"
                final_opts.append({
                    "option_key": letter,
                    "text": opt_dict["text"],
                    "original_index": opt_dict["original_index"]
                })

            output_items.append(
                ShuffledQuestionItem(
                    original_question_id=str(q.get("id", f"q_{idx}")),
                    display_index=idx + 1,
                    question_text=q.get("prompt", q.get("text", "")),
                    shuffled_options=final_opts,
                    points=float(q.get("points", 1.0))
                )
            )

        return output_items
