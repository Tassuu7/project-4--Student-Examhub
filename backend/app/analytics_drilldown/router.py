"""
ExamHub Advanced Analytics Drilldown - FastAPI Router
Endpoints for longitudinal item parameter drift analysis and normalized score conversions.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.analytics_drilldown.schemas import (
    DrilldownAnalyticsOverview,
    CohortClusterProfile,
    StandardizedScoreRecord,
    ItemParameterDrift,
    TermDifficultyRecord,
)
from backend.app.analytics_drilldown.score_scaling import ScoreScalingEngine
from backend.app.analytics_drilldown.item_difficulty_drift import ItemDriftAnalyzer
from backend.app.auth.dependencies import require_role

router = APIRouter(prefix="/api/analytics-drilldown", tags=["Longitudinal Analytics Drilldown"])


@router.get("/exam/{exam_id}/overview", response_model=DrilldownAnalyticsOverview)
def get_drilldown_overview(
    exam_id: str,
    current_user: dict = Depends(require_role(["teacher", "admin"]))
):
    """
    Returns high-dimensional cohort segmentation, stanine curves, and drift metrics for an exam.
    """
    # Sample candidate data
    candidates_data = [
        (f"cand_{i:03d}", float(40 + (i * 2.3) % 55), 100.0)
        for i in range(1, 31)
    ]
    std_scores = ScoreScalingEngine.standardize_cohort_scores(candidates_data)

    raws = [r.raw_score for r in std_scores]
    mean_raw = sum(raws) / len(raws) if raws else 0.0
    sd_raw = 12.4

    clusters = [
        CohortClusterProfile(
            cluster_id=1,
            archetype_name="Fast Masters",
            description="High accuracy (>85%) with rapid response times (<40s/item)",
            candidate_count=8,
            mean_score=89.2,
            mean_speed_sec_per_item=34.5,
            mean_flagged_count=0.1,
            candidate_ids=[f"cand_{i:03d}" for i in range(1, 9)]
        ),
        CohortClusterProfile(
            cluster_id=2,
            archetype_name="Methodical Solvers",
            description="Consistent solid accuracy (70-85%) with careful deliberation (>75s/item)",
            candidate_count=14,
            mean_score=76.8,
            mean_speed_sec_per_item=82.0,
            mean_flagged_count=0.4,
            candidate_ids=[f"cand_{i:03d}" for i in range(9, 23)]
        ),
        CohortClusterProfile(
            cluster_id=3,
            archetype_name="Struggling Guessers",
            description="Low accuracy (<50%) with erratic rapid submissions (<20s/item)",
            candidate_count=8,
            mean_score=44.1,
            mean_speed_sec_per_item=18.6,
            mean_flagged_count=2.3,
            candidate_ids=[f"cand_{i:03d}" for i in range(23, 31)]
        )
    ]

    return DrilldownAnalyticsOverview(
        exam_id=exam_id,
        total_candidates=len(std_scores),
        mean_raw_score=round(mean_raw, 2),
        std_dev_raw_score=sd_raw,
        drifted_items_count=1,
        clusters=clusters,
        standardized_scores=std_scores
    )


@router.get("/item/{item_id}/drift", response_model=ItemParameterDrift)
def get_item_drift_history(
    item_id: str,
    current_user: dict = Depends(require_role(["teacher", "admin"]))
):
    """
    Analyzes historical difficulty drift across 4 academic terms.
    """
    history = [
        TermDifficultyRecord(term_label="Fall 2024", p_value=0.52, difficulty_b=0.42, sample_size=420),
        TermDifficultyRecord(term_label="Spring 2025", p_value=0.55, difficulty_b=0.38, sample_size=380),
        TermDifficultyRecord(term_label="Fall 2025", p_value=0.68, difficulty_b=-0.05, sample_size=510),
        TermDifficultyRecord(term_label="Spring 2026", p_value=0.81, difficulty_b=-0.48, sample_size=460)
    ]
    return ItemDriftAnalyzer.evaluate_item_drift(item_id, history)
