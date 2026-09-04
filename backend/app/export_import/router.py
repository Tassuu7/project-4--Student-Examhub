"""
ExamHub - Data Exchange & Batch Ingestion API Router
Exposes endpoints for CSV rosters, question bank backups, and Aiken/GIFT parsers.
"""

from fastapi import APIRouter, Depends, Response
from fastapi.responses import PlainTextResponse, JSONResponse
from typing import Dict, Any

from backend.app.auth.dependencies import get_current_user
from backend.app.auth.rbac import require_role
from backend.app.export_import.schemas import AikenImportRequest, AikenImportResult
from backend.app.export_import.csv_exporter import CsvExporter
from backend.app.export_import.json_exporter import JsonArchiveExporter
from backend.app.export_import.aiken_parser import AikenParser

router = APIRouter(prefix="/export-import", tags=["Data Export & Ingestion"])

@router.get("/exam/{exam_id}/csv")
def export_exam_results_csv(
    exam_id: str,
    current_user: Dict[str, Any] = Depends(require_role(["admin", "teacher"]))
):
    """Export complete exam scorecard roster as an Excel-compatible UTF-8 CSV."""
    csv_data = CsvExporter.export_exam_results_csv(exam_id)
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=exam_{exam_id}_results.csv"}
    )

@router.get("/subject/{subject_id}/questions/csv")
def export_subject_questions_csv(
    subject_id: str,
    current_user: Dict[str, Any] = Depends(require_role(["admin", "teacher"]))
):
    """Export full subject question bank as CSV."""
    csv_data = CsvExporter.export_question_bank_csv(subject_id)
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=subject_{subject_id}_questions.csv"}
    )

@router.get("/exam/{exam_id}/archive")
def export_exam_json_archive(
    exam_id: str,
    current_user: Dict[str, Any] = Depends(require_role(["admin", "teacher"]))
):
    """Export complete JSON exam archive containing questions, options, and settings."""
    archive = JsonArchiveExporter.export_exam_package(exam_id)
    return JSONResponse(content=archive)

@router.post("/import/aiken", response_model=AikenImportResult)
def import_aiken_questions(
    payload: AikenImportRequest,
    current_user: Dict[str, Any] = Depends(require_role(["admin", "teacher"]))
):
    """Batch import multiple-choice questions in standard Aiken text format."""
    result = AikenParser.import_aiken_questions(
        subject_id=payload.subject_id,
        raw_text=payload.aiken_text,
        default_difficulty=payload.default_difficulty or "Medium",
        default_marks=payload.default_marks or 1.0,
        topic=payload.topic or "General",
        teacher_id=current_user.get("id")
    )
    return AikenImportResult(**result)
