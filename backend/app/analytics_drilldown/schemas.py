"""
ExamHub Advanced Analytics Drilldown - Schemas
Supports Item Parameter Drift (IPD), candidate growth percentiles, score scaling, and cohort clustering.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class TermDifficultyRecord(BaseModel):
    term_label: str  # e.g., "Fall 2024", "Spring 2025", "Fall 2025"
    p_value: float
    difficulty_b: float
    sample_size: int


class ItemParameterDrift(BaseModel):
    item_id: str
    term_history: List[TermDifficultyRecord]
    drift_delta_b: float
    is_drift_significant: bool
    drift_direction: str  # "STABLE", "EASIER" (possible leak), "HARDER"


class StandardizedScoreRecord(BaseModel):
    candidate_id: str
    raw_score: float
    percentage: float
    z_score: float
    t_score: float
    stanine: int
    percentile: float
    scaled_score_500: int


class CohortClusterProfile(BaseModel):
    cluster_id: int
    archetype_name: str
    description: str
    candidate_count: int
    mean_score: float
    mean_speed_sec_per_item: float
    mean_flagged_count: float
    candidate_ids: List[str]


class DrilldownAnalyticsOverview(BaseModel):
    exam_id: str
    total_candidates: int
    mean_raw_score: float
    std_dev_raw_score: float
    drifted_items_count: int
    clusters: List[CohortClusterProfile]
    standardized_scores: List[StandardizedScoreRecord]
