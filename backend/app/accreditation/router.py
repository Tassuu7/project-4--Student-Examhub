"""
ExamHub Accreditation & Outcome-Based Education - FastAPI Router
Endpoints for evaluating course outcome attainment and generating PO correlation matrices.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from backend.app.accreditation.schemas import (
    CourseOutcome,
    ProgramOutcome,
    CO_PO_Correlation,
    StudentAssessmentRecord,
    POAttainmentMatrix,
    AccreditationStandard,
)
from backend.app.accreditation.naac_nba_engine import NBAAttainmentEngine
from backend.app.auth.dependencies import require_role

router = APIRouter(prefix="/api/accreditation", tags=["Accreditation & OBE"])


class ComputeAttainmentRequest(BaseModel):
    course_id: str
    standard: AccreditationStandard = AccreditationStandard.NBA
    outcomes: List[CourseOutcome]
    correlations: List[CO_PO_Correlation]
    assessment_records: List[StudentAssessmentRecord]


@router.post("/compute-attainment", response_model=POAttainmentMatrix)
def compute_attainment(
    req: ComputeAttainmentRequest,
    current_user: dict = Depends(require_role(["teacher", "admin"]))
):
    """
    Compute Course Outcome attainment levels and Program Outcome correlation scores.
    """
    co_results = []
    for co in req.outcomes:
        res = NBAAttainmentEngine.calculate_co_attainment(co, req.assessment_records)
        co_results.append(res)

    matrix = NBAAttainmentEngine.compute_po_attainment(
        course_id=req.course_id,
        co_results=co_results,
        correlations=req.correlations,
        standard=req.standard
    )
    return matrix


@router.get("/sample-matrix", response_model=POAttainmentMatrix)
def get_sample_matrix(current_user: dict = Depends(require_role(["teacher", "admin"]))):
    """
    Return demonstration matrix for Computer Science & Engineering course (CS301).
    """
    outcomes = [
        CourseOutcome(co_code="CO1", description="Understand distributed consensus", target_percentage=70.0, target_threshold_score=60.0),
        CourseOutcome(co_code="CO2", description="Design high-concurrency microservices", target_percentage=75.0, target_threshold_score=65.0),
        CourseOutcome(co_code="CO3", description="Implement fault-tolerant storage", target_percentage=70.0, target_threshold_score=60.0),
    ]
    correlations = [
        CO_PO_Correlation(co_code="CO1", po_code="PO1", correlation_level=3),
        CO_PO_Correlation(co_code="CO1", po_code="PO2", correlation_level=2),
        CO_PO_Correlation(co_code="CO2", po_code="PO1", correlation_level=2),
        CO_PO_Correlation(co_code="CO2", po_code="PO3", correlation_level=3),
        CO_PO_Correlation(co_code="CO3", po_code="PO2", correlation_level=3),
        CO_PO_Correlation(co_code="CO3", po_code="PO3", correlation_level=3),
    ]

    # Sample student data
    records = []
    for sid in range(1, 41):
        # CO1
        records.append(StudentAssessmentRecord(
            student_id=f"STU_{sid:03d}", assessment_type="Midterm", question_id="Q1",
            co_code="CO1", max_marks=20.0, obtained_marks=14.0 + (sid % 6)
        ))
        # CO2
        records.append(StudentAssessmentRecord(
            student_id=f"STU_{sid:03d}", assessment_type="Final", question_id="Q2",
            co_code="CO2", max_marks=30.0, obtained_marks=20.0 + (sid % 9)
        ))
        # CO3
        records.append(StudentAssessmentRecord(
            student_id=f"STU_{sid:03d}", assessment_type="Final", question_id="Q3",
            co_code="CO3", max_marks=25.0, obtained_marks=16.0 + (sid % 8)
        ))

    co_results = [NBAAttainmentEngine.calculate_co_attainment(co, records) for co in outcomes]
    return NBAAttainmentEngine.compute_po_attainment(
        course_id="CS301-Distributed-Systems",
        co_results=co_results,
        correlations=correlations,
        standard=AccreditationStandard.NBA
    )
