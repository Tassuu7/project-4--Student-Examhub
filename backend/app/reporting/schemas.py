"""
ExamHub Institutional Reporting & Transcripts - Schemas
Defines request and response schemas for printable institutional reports,
student transcripts, and accreditation audit summaries.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class CandidateTranscriptItem(BaseModel):
    subject_code: str
    subject_name: str
    credits: float
    grade_letter: str
    grade_points: float
    percentage: float
    status: str  # PASS / FAIL


class CandidateOfficialTranscript(BaseModel):
    transcript_id: str
    candidate_id: str
    candidate_name: str
    institution_name: str
    enrollment_number: str
    program_name: str
    gpa: float
    cgpa: float
    total_credits: float
    issued_date: str
    verification_hash: str
    items: List[CandidateTranscriptItem]


class InstitutionalExamSummaryReport(BaseModel):
    exam_id: str
    exam_title: str
    academic_term: str
    total_registered: int
    total_attended: int
    absent_count: int
    mean_score: float
    median_score: float
    std_dev: float
    highest_score: float
    lowest_score: float
    pass_percentage: float
    grade_counts: Dict[str, int]
    generated_at: str
    generated_by: str
