"""
ExamHub - Analytics and Psychometrics API Router
Exposes endpoints for exam score distributions, item response metrics,
system-wide KPIs, and cohort hypothesis testing.
"""

from fastapi import APIRouter, Depends, Query
from typing import Dict, Any

from backend.app.auth.dependencies import get_current_user
from backend.app.auth.rbac import require_role
from backend.app.analytics.schemas import (
    ExamAnalyticsResponse, SystemOverviewAnalytics,
    CohortComparisonRequest, CohortComparisonResult
)
from backend.app.analytics.service import AnalyticsService
from backend.app.analytics.trend_analyzer import TrendAnalyzer
from backend.app.analytics.cohort_comparison import CohortComparisonEngine

router = APIRouter(prefix="/analytics", tags=["Analytics & Psychometrics"])

@router.get("/exam/{exam_id}", response_model=ExamAnalyticsResponse)
def get_exam_analytics(
    exam_id: str,
    current_user: Dict[str, Any] = Depends(require_role(["admin", "teacher"]))
):
    """Retrieve full psychometric item analysis, score distributions, and rankings for an exam."""
    return AnalyticsService.get_exam_analytics(exam_id)

@router.get("/overview", response_model=SystemOverviewAnalytics)
def get_system_overview(
    current_user: Dict[str, Any] = Depends(require_role(["admin", "teacher"]))
):
    """Retrieve global system KPIs, average pass rates, and active assessment stats."""
    return AnalyticsService.get_system_overview()

@router.get("/student/{student_id}/trend")
def get_student_trend(
    student_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Retrieve longitudinal performance trajectory for a specific student."""
    return TrendAnalyzer.get_student_trend(student_id)

@router.get("/subject/{subject_id}/trend")
def get_subject_trend(
    subject_id: str,
    current_user: Dict[str, Any] = Depends(require_role(["admin", "teacher"]))
):
    """Retrieve historical assessment performance trends for a curriculum subject."""
    return TrendAnalyzer.get_subject_longitudinal_trend(subject_id)

@router.post("/compare-cohorts", response_model=CohortComparisonResult)
def compare_cohorts(
    payload: CohortComparisonRequest,
    current_user: Dict[str, Any] = Depends(require_role(["admin", "teacher"]))
):
    """Perform statistical hypothesis testing (Welch's t-test, Cohen's d) between two exam cohorts."""
    return CohortComparisonEngine.compare_cohorts(
        payload.cohort_a_exam_id,
        payload.cohort_b_exam_id
    )
