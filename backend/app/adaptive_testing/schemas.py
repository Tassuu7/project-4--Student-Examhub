"""
ExamHub Computerized Adaptive Testing (CAT) System - Schemas
Defines request, response, and domain models for Item Response Theory (IRT)
based adaptive testing workflows, theta tracking, and stopping criteria.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum


class StoppingRuleType(str, Enum):
    FIXED_LENGTH = "fixed_length"
    SEM_THRESHOLD = "sem_threshold"
    COMBINED = "combined"
    TIME_EXHAUSTION = "time_exhaustion"


class AbilityEstimationMethod(str, Enum):
    EAP = "expected_a_posteriori"
    MLE = "maximum_likelihood_estimation"
    MAP = "maximum_a_posteriori"


class CATItemParameter(BaseModel):
    item_id: str
    difficulty_b: float = Field(..., description="Item difficulty parameter (b) in logits, typically -3.0 to +3.0")
    discrimination_a: float = Field(default=1.0, ge=0.01, le=4.0, description="Item discrimination parameter (a)")
    guessing_c: float = Field(default=0.0, ge=0.0, le=0.5, description="Item pseudo-guessing parameter (c)")
    slipping_s: float = Field(default=0.0, ge=0.0, le=0.3, description="Item slipping parameter (s)")
    domain_content: str = Field(default="general", description="Subject area or learning objective category")
    question_text: str = Field(default="", description="Question prompt content")
    options: List[str] = Field(default_factory=list)
    correct_option_index: int = Field(default=0)


class CATSessionConfig(BaseModel):
    min_items: int = Field(default=10, ge=3, le=100)
    max_items: int = Field(default=35, ge=5, le=150)
    target_sem: float = Field(default=0.30, ge=0.10, le=1.0)
    initial_theta: float = Field(default=0.0, ge=-4.0, le=4.0)
    estimation_method: AbilityEstimationMethod = AbilityEstimationMethod.EAP
    stopping_rule: StoppingRuleType = StoppingRuleType.COMBINED
    content_balancing: bool = Field(default=True)
    exposure_control_rate: float = Field(default=0.30, ge=0.05, le=1.0)


class CandidateResponseRecord(BaseModel):
    step_number: int
    item_id: str
    selected_option_index: int
    is_correct: bool
    response_time_seconds: float
    difficulty_b: float
    discrimination_a: float
    guessing_c: float
    theta_prior: float
    theta_post: float
    sem_post: float


class CATSessionState(BaseModel):
    session_id: str
    candidate_id: str
    exam_id: str
    config: CATSessionConfig
    current_step: int = 0
    current_theta: float = 0.0
    current_sem: float = 1.0
    responses: List[CandidateResponseRecord] = Field(default_factory=list)
    administered_item_ids: List[str] = Field(default_factory=list)
    is_completed: bool = False
    termination_reason: Optional[str] = None
    started_at: str
    completed_at: Optional[str] = None
    percentile_rank: Optional[float] = None


class NextItemRequest(BaseModel):
    session_id: str


class NextItemResponse(BaseModel):
    session_id: str
    step_number: int
    is_completed: bool
    item_id: Optional[str] = None
    question_text: Optional[str] = None
    options: List[str] = Field(default_factory=list)
    current_theta: float
    current_sem: float
    total_administered: int
    termination_reason: Optional[str] = None


class SubmitCATAnswerRequest(BaseModel):
    session_id: str
    item_id: str
    selected_option_index: int
    response_time_seconds: float = 0.0


class SubmitCATAnswerResponse(BaseModel):
    session_id: str
    step_number: int
    is_correct: bool
    updated_theta: float
    updated_sem: float
    is_completed: bool
    termination_reason: Optional[str] = None


class CATSimulationRequest(BaseModel):
    true_thetas: List[float] = Field(default_factory=lambda: [-2.0, -1.0, 0.0, 1.0, 2.0])
    pool_size: int = Field(default=100, ge=20, le=1000)
    config: CATSessionConfig = Field(default_factory=CATSessionConfig)


class CATSimulationResult(BaseModel):
    simulations_count: int
    true_theta: float
    mean_estimated_theta: float
    bias: float
    root_mean_squared_error: float
    mean_test_length: float
    mean_sem: float
