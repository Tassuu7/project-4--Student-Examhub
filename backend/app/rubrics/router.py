"""
ExamHub Rubrics - FastAPI Router
Endpoints for creating rubrics, scoring candidate open-response submissions,
and calculating inter-rater reliability metrics.
"""

import uuid
from datetime import datetime, timezone
from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.rubrics.schemas import (
    RubricDefinition,
    SubmissionGradingRequest,
    EvaluationRecord,
    InterRaterReliabilityRequest,
    InterRaterReliabilityResult,
    RubricCriterion,
    PerformanceLevel,
    RubricType,
)
from backend.app.rubrics.evaluator import RubricEvaluator
from backend.app.auth.dependencies import require_role

router = APIRouter(prefix="/api/rubrics", tags=["Rubrics & Inter-Rater Reliability"])

# In-memory storage
_RUBRICS: Dict[str, RubricDefinition] = {}
_EVALUATIONS: Dict[str, List[EvaluationRecord]] = {}  # rubric_id -> list of records


def _seed_sample_rubric():
    sample = RubricDefinition(
        rubric_id="rub-cs-capstone-01",
        title="Software Engineering Capstone Design Rubric",
        rubric_type=RubricType.ANALYTIC,
        criteria=[
            RubricCriterion(
                criterion_id="crit_arch",
                title="System Architecture & Scalability",
                weight=1.5,
                description="Evaluation of microservices decomposition and failure isolation",
                levels=[
                    PerformanceLevel(level_id="lvl_4", label="Exemplary", points=20.0, description="Flawless asynchronous decoupling and distributed state management"),
                    PerformanceLevel(level_id="lvl_3", label="Proficient", points=15.0, description="Clear modularity with minor bottleneck points"),
                    PerformanceLevel(level_id="lvl_2", label="Developing", points=10.0, description="Monolithic leakage and coupled data stores"),
                    PerformanceLevel(level_id="lvl_1", label="Novice", points=5.0, description="No modular separation or concurrency safety")
                ]
            ),
            RubricCriterion(
                criterion_id="crit_code",
                title="Code Quality & Test Coverage",
                weight=1.0,
                description="Evaluation of test suites, type safety, and linting compliance",
                levels=[
                    PerformanceLevel(level_id="lvl_4", label="Exemplary", points=20.0, description="Over 85% branch coverage, automated CI/CD gating"),
                    PerformanceLevel(level_id="lvl_3", label="Proficient", points=15.0, description="Comprehensive unit tests, lacking integration tests"),
                    PerformanceLevel(level_id="lvl_2", label="Developing", points=10.0, description="Sparse test cases, untyped interfaces"),
                    PerformanceLevel(level_id="lvl_1", label="Novice", points=5.0, description="Zero automated tests")
                ]
            )
        ]
    )
    _RUBRICS[sample.rubric_id] = sample

_seed_sample_rubric()


@router.get("/", response_model=List[RubricDefinition])
def list_rubrics(current_user: dict = Depends(require_role(["teacher", "admin"]))):
    """List all configured evaluation rubrics."""
    return list(_RUBRICS.values())


@router.post("/", response_model=RubricDefinition)
def create_rubric(
    rubric: RubricDefinition,
    current_user: dict = Depends(require_role(["teacher", "admin"]))
):
    """Create or update a grading rubric."""
    _RUBRICS[rubric.rubric_id] = rubric
    return rubric


@router.post("/grade", response_model=EvaluationRecord)
def grade_submission(
    req: SubmissionGradingRequest,
    current_user: dict = Depends(require_role(["teacher", "admin"]))
):
    """
    Score a candidate submission against an analytic or holistic rubric.
    """
    rubric = _RUBRICS.get(req.rubric_id)
    if not rubric:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rubric {req.rubric_id} not found."
        )

    tot, pct, scores_map, levels_map = RubricEvaluator.calculate_score(rubric, req.criterion_scores)

    eval_record = EvaluationRecord(
        evaluation_id=f"eval-{uuid.uuid4().hex[:10]}",
        rubric_id=req.rubric_id,
        submission_id=req.submission_id,
        candidate_id=req.candidate_id,
        evaluator_id=req.evaluator_id,
        criterion_scores=scores_map,
        criterion_levels=levels_map,
        total_score=tot,
        percentage=pct,
        general_comments=req.general_comments,
        graded_at=datetime.now(timezone.utc).isoformat()
    )

    if req.rubric_id not in _EVALUATIONS:
        _EVALUATIONS[req.rubric_id] = []
    _EVALUATIONS[req.rubric_id].append(eval_record)

    return eval_record


@router.post("/inter-rater-reliability", response_model=InterRaterReliabilityResult)
def compute_inter_rater_reliability(
    req: InterRaterReliabilityRequest,
    current_user: dict = Depends(require_role(["teacher", "admin"]))
):
    """
    Analyze marker consensus and compute Fleiss' and Cohen's Kappa for a rubric.
    """
    rubric = _RUBRICS.get(req.rubric_id)
    if not rubric:
        raise HTTPException(status_code=404, detail="Rubric not found")

    # Mock rating distribution across 4 levels
    # 10 subjects rated by 3 raters
    rating_matrix = [
        [3, 0, 0, 0],
        [2, 1, 0, 0],
        [0, 3, 0, 0],
        [0, 2, 1, 0],
        [0, 0, 3, 0],
        [0, 1, 2, 0],
        [0, 0, 0, 3],
        [0, 0, 1, 2],
        [3, 0, 0, 0],
        [0, 3, 0, 0],
    ]
    f_kappa = RubricEvaluator.calculate_fleiss_kappa(rating_matrix)
    c_kappa = RubricEvaluator.calculate_cohens_kappa([0, 1, 2, 1, 3, 2, 0, 1], [0, 1, 2, 2, 3, 2, 0, 1], 4)

    return InterRaterReliabilityResult(
        rubric_id=req.rubric_id,
        num_submissions=len(rating_matrix),
        num_raters=3,
        cohens_kappa=c_kappa,
        fleiss_kappa=f_kappa,
        interpretation=RubricEvaluator.interpret_kappa(f_kappa),
        flagged_discrepancies_count=2,
        discrepancy_details=[
            {"submission_id": "sub_102", "variance": 1.45, "raters": ["eval_1", "eval_2"]},
            {"submission_id": "sub_108", "variance": 1.62, "raters": ["eval_2", "eval_3"]}
        ]
    )
