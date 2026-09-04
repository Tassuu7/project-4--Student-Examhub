"""
ExamHub Accreditation & Outcome-Based Education (OBE) - Schemas
Supports ABET, NBA, and NAAC accreditation criteria, Course Outcome (CO) to
Program Outcome (PO) mapping matrices, and attainment evaluations.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum


class AccreditationStandard(str, Enum):
    ABET = "ABET_EAC"
    NBA = "NBA_INDIA"
    NAAC = "NAAC_CRITERIA_2"
    WASHINGTON_ACCORD = "WASHINGTON_ACCORD"


class CourseOutcome(BaseModel):
    co_code: str  # e.g., "CO1", "CO2"
    description: str
    target_percentage: float = Field(default=70.0, ge=0.0, le=100.0)
    target_threshold_score: float = Field(default=60.0, ge=0.0, le=100.0)


class ProgramOutcome(BaseModel):
    po_code: str  # e.g., "PO1" (Engineering Knowledge), "PO2" (Problem Analysis)
    title: str
    description: str


class CO_PO_Correlation(BaseModel):
    co_code: str
    po_code: str
    correlation_level: int = Field(..., ge=0, le=3, description="0=None, 1=Low, 2=Medium, 3=High")


class StudentAssessmentRecord(BaseModel):
    student_id: str
    assessment_type: str  # e.g., "Midterm", "Final", "Assignment"
    question_id: str
    co_code: str
    max_marks: float
    obtained_marks: float


class COAttainmentResult(BaseModel):
    co_code: str
    total_students: int
    students_above_threshold: int
    direct_attainment_percentage: float
    attainment_level: int = Field(..., ge=0, le=3)  # Level 1 (>=60%), Level 2 (>=70%), Level 3 (>=80%)
    target_met: bool


class POAttainmentMatrix(BaseModel):
    course_id: str
    standard: AccreditationStandard
    co_results: List[COAttainmentResult]
    po_scores: Dict[str, float]  # po_code -> computed attainment score (0.0 to 3.0)
    matrix_table: List[Dict[str, Any]]
    recommendations: List[str] = Field(default_factory=list)
