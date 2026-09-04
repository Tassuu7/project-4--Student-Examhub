"""
ExamHub Numerical Tolerance Question Engine
Parses candidate numerical answers, handles units, scientific notation, and tolerance boundaries.
"""

import re
import math
from typing import Tuple, Optional
from backend.app.question_engines.schemas import (
    NumericalGradingRequest,
    NumericalGradingResponse,
    ToleranceType,
)


class NumericalEngine:
    """
    Evaluates STEM numerical answers with tolerances, unit parsing, and significant figures.
    """

    UNIT_REGEX = re.compile(r"^([+-]?\d*(?:\.\d+)?(?:[eE][+-]?\d+)?)\s*([a-zA-Z/^_]+)?$")

    @classmethod
    def parse_candidate_input(cls, text: str) -> Tuple[Optional[float], Optional[str]]:
        """
        Parses numeric input string into (float_value, unit_string).
        """
        text = text.strip()
        match = cls.UNIT_REGEX.match(text)
        if not match:
            return None, None

        val_str, unit_str = match.groups()
        if not val_str:
            return None, None

        try:
            val = float(val_str)
            unit = unit_str.strip() if unit_str else None
            return val, unit
        except ValueError:
            return None, None

    @classmethod
    def count_significant_figures(cls, num_str: str) -> int:
        """
        Counts significant figures in a formatted numeric string.
        """
        s = num_str.strip().lower()
        if "e" in s:
            s = s.split("e")[0]
        s = s.lstrip("+-").lstrip("0")
        if not s:
            return 1
        if "." in s:
            # Leading zeros after decimal if no whole part
            s = s.replace(".", "")
            s = s.lstrip("0")
            return len(s) if s else 1
        else:
            return len(s.rstrip("0")) if s.rstrip("0") else 1

    @classmethod
    def evaluate(cls, req: NumericalGradingRequest) -> NumericalGradingResponse:
        val, unit = cls.parse_candidate_input(req.candidate_answer)

        if val is None:
            return NumericalGradingResponse(
                is_correct=False,
                score=0.0,
                feedback="Could not parse candidate answer as a valid number."
            )

        # Check unit if required
        if req.required_unit:
            if not unit or unit.lower() != req.required_unit.lower():
                return NumericalGradingResponse(
                    is_correct=False,
                    score=0.0,
                    parsed_value=val,
                    parsed_unit=unit,
                    feedback=f"Incorrect or missing unit. Expected '{req.required_unit}', got '{unit}'."
                )

        # Check tolerance
        target = req.target_value
        is_in_bounds = False

        if req.tolerance_type == ToleranceType.ABSOLUTE:
            diff = abs(val - target)
            is_in_bounds = (diff <= req.tolerance)
        elif req.tolerance_type == ToleranceType.RELATIVE_PERCENTAGE:
            if abs(target) < 1e-9:
                is_in_bounds = (abs(val) <= req.tolerance)
            else:
                rel_diff = abs(val - target) / abs(target)
                is_in_bounds = (rel_diff <= req.tolerance)
        elif req.tolerance_type == ToleranceType.SIGNIFICANT_FIGURES:
            if req.sig_figs:
                figs = cls.count_significant_figures(req.candidate_answer.split()[0])
                diff = abs(val - target) / max(1e-9, abs(target))
                is_in_bounds = (diff <= 0.02 and figs == req.sig_figs)
            else:
                is_in_bounds = (abs(val - target) <= 0.01)

        if is_in_bounds:
            return NumericalGradingResponse(
                is_correct=True,
                score=1.0,
                parsed_value=val,
                parsed_unit=unit,
                feedback="Correct! Answer satisfies required tolerance boundaries."
            )
        else:
            return NumericalGradingResponse(
                is_correct=False,
                score=0.0,
                parsed_value=val,
                parsed_unit=unit,
                feedback=f"Answer {val} is outside acceptable range of target {target} (tolerance: {req.tolerance})."
            )
