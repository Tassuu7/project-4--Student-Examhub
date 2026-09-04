"""
ExamHub Rubrics and Inter-Rater Reliability - Schemas
Supports analytic, holistic, and developmental rubrics with multi-marker consensus workflows.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum


class RubricType(str, Enum):
    ANALYTIC = "analytic"
    HOLISTIC = "holistic"
    DEVELOPMENTAL = "developmental"


class PerformanceLevel(BaseModel):
    level_id: str
    label: str  # e.g., "Exemplary", "Proficient", "Developing", "Novice"
    points: float
    description: str


class RubricCriterion(BaseModel):
    criterion_id: str
    title: str
    weight: float = Field(default=1.0, ge=0.01, le=10.0)
    description: str = ""
    levels: List[PerformanceLevel] = Field(default_factory=list)


class RubricDefinition(BaseModel):
    rubric_id: str
    exam_id: Optional[str] = None
    question_id: Optional[str] = None
    title: str
    rubric_type: RubricType = RubricType.ANALYTIC
    criteria: List[RubricCriterion] = Field(default_factory=list)
    max_total_points: float = 100.0


class CriterionScoreInput(BaseModel):
    criterion_id: str
    selected_level_id: str
    feedback_notes: Optional[str] = None
    adjusted_score: Optional[float] = None


class SubmissionGradingRequest(BaseModel):
    rubric_id: str
    submission_id: str
    candidate_id: str
    evaluator_id: str
    criterion_scores: List[CriterionScoreInput]
    general_comments: Optional[str] = None


class EvaluationRecord(BaseModel):
    evaluation_id: str
    rubric_id: str
    submission_id: str
    candidate_id: str
    evaluator_id: str
    criterion_scores: Dict[str, float]  # criterion_id -> numeric score
    criterion_levels: Dict[str, str]   # criterion_id -> level_id
    total_score: float
    percentage: float
    general_comments: Optional[str] = None
    graded_at: str


class InterRaterReliabilityRequest(BaseModel):
    rubric_id: str
    submission_ids: List[str]
    evaluator_ids: List[str]


class InterRaterReliabilityResult(BaseModel):
    rubric_id: str
    num_submissions: int
    num_raters: int
    cohens_kappa: Optional[float] = None
    fleiss_kappa: Optional[float] = None
    interpretation: str
    flagged_discrepancies_count: int
    discrepancy_details: List[Dict[str, Any]] = Field(default_factory=list)
