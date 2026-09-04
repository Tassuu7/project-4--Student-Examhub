"""
ExamHub - Grading & Normalization API Router
Endpoints for grade curves, manual remark adjustments, and rubrics.
"""

from fastapi import APIRouter, Depends
from typing import Dict, Any

from backend.app.auth.rbac import require_role
from backend.app.grading.schemas import (
    GradeCurveRequest, GradeCurveResult, ScoreAdjustmentRequest
)
from backend.app.grading.service import GradingService

router = APIRouter(prefix="/grading", tags=["Grading & Score Curves"])

@router.post("/curve", response_model=GradeCurveResult)
def apply_grade_curve(
    payload: GradeCurveRequest,
    current_user: Dict[str, Any] = Depends(require_role(["admin", "teacher"]))
):
    """Teacher/Admin: Apply mathematical curve adjustment (square_root, linear_offset, bell_curve)."""
    return GradingService.apply_curve(
        payload.exam_id,
        payload.method,
        payload.target_mean
    )

@router.post("/adjust")
def adjust_candidate_score(
    payload: ScoreAdjustmentRequest,
    current_user: Dict[str, Any] = Depends(require_role(["admin", "teacher"]))
):
    """Teacher/Admin: Manually override/moderate score on a specific question with audit reason."""
    return GradingService.adjust_single_score(
        payload.model_dump(),
        current_user["id"]
    )
