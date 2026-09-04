"""
ExamHub Advanced Question Engines - Schemas
Supports numerical with tolerance, cloze fill-in-blanks, ordering permutations, and coordinate hotspot items.
"""

from typing import List, Dict, Optional, Tuple, Any
from pydantic import BaseModel, Field
from enum import Enum


class ToleranceType(str, Enum):
    ABSOLUTE = "absolute"
    RELATIVE_PERCENTAGE = "relative_percentage"
    SIGNIFICANT_FIGURES = "significant_figures"


class NumericalGradingRequest(BaseModel):
    candidate_answer: str
    target_value: float
    tolerance: float = 0.05
    tolerance_type: ToleranceType = ToleranceType.RELATIVE_PERCENTAGE
    required_unit: Optional[str] = None
    sig_figs: Optional[int] = None


class NumericalGradingResponse(BaseModel):
    is_correct: bool
    score: float
    parsed_value: Optional[float] = None
    parsed_unit: Optional[str] = None
    feedback: str


class ClozeGapRule(BaseModel):
    gap_index: int
    acceptable_answers: List[str]
    case_sensitive: bool = False
    allow_typo_distance: int = 0  # Max Levenshtein edit distance
    regex_pattern: Optional[str] = None


class ClozeGradingRequest(BaseModel):
    candidate_answers: Dict[int, str]  # gap_index -> answer
    gap_rules: List[ClozeGapRule]


class ClozeGradingResponse(BaseModel):
    total_gaps: int
    correct_gaps: int
    score_percentage: float
    gap_results: Dict[int, bool]
    feedback_per_gap: Dict[int, str]


class OrderingGradingRequest(BaseModel):
    candidate_order: List[str]
    correct_order: List[str]
    scoring_method: str = "kendalls_tau"  # kendalls_tau, exact, spearman


class OrderingGradingResponse(BaseModel):
    is_perfect: bool
    partial_score: float
    kendall_tau: float
    spearman_rho: float


class Point2D(BaseModel):
    x: float
    y: float


class HotspotGradingRequest(BaseModel):
    click_point: Point2D
    target_polygon: List[Point2D]


class HotspotGradingResponse(BaseModel):
    is_hit: bool
    score: float
    click_coordinates: Point2D
