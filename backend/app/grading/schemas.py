"""
ExamHub - Grading Rubrics & Score Normalization Schemas
Data contracts for rubric evaluation, score adjustments, curve transformations,
and post-submission moderation.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class RubricLevel(BaseModel):
    level_name: str  # Exemplary, Competent, Developing, Inadequate
    score: float
    description: str

class RubricCriterion(BaseModel):
    id: str
    name: str
    weight: float = Field(default=1.0, ge=0.1)
    max_score: float
    levels: List[RubricLevel]

class ExamRubricDefinition(BaseModel):
    id: str
    exam_id: str
    name: str
    description: Optional[str] = None
    criteria: List[RubricCriterion]
    total_rubric_marks: float

class NegativeMarkingConfig(BaseModel):
    exam_id: str
    enabled: bool = False
    penalty_fraction: float = Field(default=0.25, ge=0.0, le=1.0)  # e.g., 0.25 = 1/4th mark deduction
    apply_to_unanswered: bool = False

class GradeCurveRequest(BaseModel):
    exam_id: str
    method: str = Field(..., description="linear_offset, square_root, normal_distribution, bell_curve")
    target_mean: Optional[float] = None
    scale_factor: Optional[float] = None

class GradeCurveResult(BaseModel):
    exam_id: str
    method: str
    original_mean: float
    curved_mean: float
    adjusted_scores_count: int
    score_deltas: List[Dict[str, Any]]

class ScoreAdjustmentRequest(BaseModel):
    attempt_id: str
    question_id: str
    new_marks: float
    adjustment_reason: str
    reviewer_notes: Optional[str] = None
