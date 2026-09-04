"""
ExamHub - Moodle GIFT Format Question Parser
Parses GIFT question files into multiple-choice and true-false questions.
Format:
::Title:: Question text { =Correct answer ~Wrong option 1 ~Wrong option 2 }
"""

import re
import uuid
from typing import List, Dict, Any, Tuple
from datetime import datetime
from backend.app.database.connection import get_db_connection

class GiftParser:
    """Parses Moodle GIFT format question syntax."""

    @staticmethod
    def parse_gift_text(raw_text: str) -> List[Dict[str, Any]]:
        questions = []
        blocks = raw_text.strip().split('\n\n')

        for block in blocks:
            b = block.strip()
            if not b or b.startswith('//'):
                continue

            # Extract optional ::Title::
            title_match = re.match(r'^::(.*?)::(.*)', b, re.DOTALL)
            if title_match:
                title = title_match.group(1).strip()
                rest = title_match.group(2).strip()
            else:
                title = ""
                rest = b

            # Extract body and answers { ... }
            body_match = re.search(r'^(.*?)\{(.*?)\}(.*)$', rest, re.DOTALL)
            if not body_match:
                continue

            q_text = body_match.group(1).strip()
            answers_part = body_match.group(2).strip()

            # Parse choices
            # =Correct option, ~Wrong option
            options = []
            correct_letter = 'A'

            parts = re.split(r'(?=[=~])', answers_part)
            clean_parts = [p.strip() for p in parts if p.strip()]

            if len(clean_parts) >= 2:
                letters = ['A', 'B', 'C', 'D']
                opt_dict = {}
                for idx, p in enumerate(clean_parts[:4]):
                    let = letters[idx]
                    is_corr = p.startswith('=')
                    val = p[1:].strip()
                    opt_dict[let] = val
                    if is_corr:
                        correct_letter = let

                while len(opt_dict) < 4:
                    missing_let = letters[len(opt_dict)]
                    opt_dict[missing_let] = "N/A"

                questions.append({
                    "title": title,
                    "question_text": q_text,
                    "option_a": opt_dict.get("A", "N/A"),
                    "option_b": opt_dict.get("B", "N/A"),
                    "option_c": opt_dict.get("C", "N/A"),
                    "option_d": opt_dict.get("D", "N/A"),
                    "correct_answer": correct_letter
                })

        return questions
