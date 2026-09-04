"""
ExamHub Institutional Reporting - FastAPI Router
Endpoints for downloading student transcripts, HTML audit documents, and CSV analytics matrices.
"""

import hashlib
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Response
from backend.app.reporting.schemas import (
    CandidateOfficialTranscript,
    CandidateTranscriptItem,
    InstitutionalExamSummaryReport,
)
from backend.app.reporting.pdf_report_generator import ReportDocumentGenerator
from backend.app.reporting.tabular_analytics import TabularAnalyticsExporter
from backend.app.auth.dependencies import get_current_user, require_role

router = APIRouter(prefix="/api/reports", tags=["Institutional Reports & Transcripts"])


@router.get("/transcript/{candidate_id}/html")
def get_candidate_transcript_html(
    candidate_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Generate official printable academic transcript HTML.
    """
    raw_hash = hashlib.sha256(f"transcript-{candidate_id}-official".encode()).hexdigest()

    transcript = CandidateOfficialTranscript(
        transcript_id=f"TRX-2026-{candidate_id.upper()}",
        candidate_id=candidate_id,
        candidate_name="Alex Vance",
        institution_name="Global Institute of Technology",
        enrollment_number=f"ENR-9982-{candidate_id}",
        program_name="Bachelor of Science in Computer Engineering",
        gpa=3.85,
        cgpa=3.92,
        total_credits=24.0,
        issued_date=datetime.now(timezone.utc).strftime("%B %d, %Y"),
        verification_hash=raw_hash,
        items=[
            CandidateTranscriptItem(subject_code="CS101", subject_name="Data Structures & Algorithms", credits=4.0, grade_letter="A", grade_points=4.0, percentage=94.5, status="PASS"),
            CandidateTranscriptItem(subject_code="CS202", subject_name="Computer Systems Architecture", credits=4.0, grade_letter="A", grade_points=4.0, percentage=91.0, status="PASS"),
            CandidateTranscriptItem(subject_code="CS303", subject_name="Distributed Cloud Computing", credits=4.0, grade_letter="A-", grade_points=3.7, percentage=88.5, status="PASS"),
            CandidateTranscriptItem(subject_code="CS404", subject_name="Cryptography & Cyber Security", credits=4.0, grade_letter="A", grade_points=4.0, percentage=96.0, status="PASS"),
            CandidateTranscriptItem(subject_code="MA201", subject_name="Discrete Applied Mathematics", credits=4.0, grade_letter="B+", grade_points=3.3, percentage=83.0, status="PASS"),
            CandidateTranscriptItem(subject_code="SE499", subject_name="Senior Capstone Project", credits=4.0, grade_letter="A", grade_points=4.0, percentage=98.0, status="PASS"),
        ]
    )

    html_content = ReportDocumentGenerator.render_candidate_transcript_html(transcript)
    return Response(content=html_content, media_type="text/html")


@router.get("/exam/{exam_id}/matrix-csv")
def download_exam_matrix_csv(
    exam_id: str,
    current_user: dict = Depends(require_role(["teacher", "admin"]))
):
    """
    Download student response matrix CSV for classical psychometric analysis.
    """
    candidates = [f"STU_{i:03d}" for i in range(1, 26)]
    questions = [f"Q_{j:02d}" for j in range(1, 11)]

    matrix = {}
    for i, c in enumerate(candidates):
        matrix[c] = {}
        for j, q in enumerate(questions):
            # Simulated responses
            matrix[c][q] = 1 if ((i + j) % 3 != 0) else 0

    csv_data = TabularAnalyticsExporter.export_cohort_responses_matrix_csv(candidates, questions, matrix)

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=exam_{exam_id}_matrix.csv"}
    )
