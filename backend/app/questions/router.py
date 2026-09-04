"""
ExamHub - Question Bank Endpoints
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Response
from backend.app.questions.schemas import QuestionCreateRequest, QuestionUpdateRequest, QuestionResponse, BulkImportSummary
from backend.app.questions.service import QuestionService
from backend.app.auth.dependencies import require_teacher, require_any_authenticated
from backend.app.auth.schemas import TokenData
from backend.app.core.constants import QuestionDifficulty
from backend.app.core.pagination import PaginationParams, PaginatedResponse
from backend.app.core.exceptions import ExamHubException

router = APIRouter(prefix="/questions", tags=["Question Bank"])

@router.get("", response_model=PaginatedResponse[QuestionResponse])
def list_questions(
    subject_id: Optional[str] = None,
    difficulty: Optional[QuestionDifficulty] = None,
    topic: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user: TokenData = Depends(require_any_authenticated)
):
    params = PaginationParams(page=page, page_size=page_size)
    return QuestionService.list_questions(
        subject_id=subject_id,
        difficulty=difficulty,
        topic=topic,
        search=search,
        teacher_id=None,
        params=params
    )

@router.post("", response_model=QuestionResponse)
def create_question(dto: QuestionCreateRequest, user: TokenData = Depends(require_teacher)):
    try:
        teacher_id = getattr(user, "teacher_id", None)
        return QuestionService.create_question(dto, teacher_id=teacher_id)
    except ExamHubException as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())

@router.get("/template.csv")
def download_csv_template(user: TokenData = Depends(require_teacher)):
    template = QuestionService.get_csv_template()
    return Response(
        content=template,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=examhub_questions_template.csv"}
    )

@router.get("/export.csv")
def export_questions_csv(subject_id: Optional[str] = None, user: TokenData = Depends(require_teacher)):
    csv_data = QuestionService.export_to_csv(subject_id=subject_id)
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=examhub_questions_export.csv"}
    )

@router.post("/import", response_model=BulkImportSummary)
async def import_questions_csv(file: UploadFile = File(...), user: TokenData = Depends(require_teacher)):
    try:
        content = await file.read()
        text_content = content.decode("utf-8-sig", errors="replace")
        teacher_id = getattr(user, "teacher_id", None)
        return QuestionService.import_from_csv(text_content, teacher_id=teacher_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail={"error": f"Failed to import questions: {str(e)}"})

@router.get("/{question_id}", response_model=QuestionResponse)
def get_question(question_id: str, user: TokenData = Depends(require_any_authenticated)):
    try:
        return QuestionService.get_question(question_id)
    except ExamHubException as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())

@router.put("/{question_id}", response_model=QuestionResponse)
def update_question(question_id: str, dto: QuestionUpdateRequest, user: TokenData = Depends(require_teacher)):
    try:
        return QuestionService.update_question(question_id, dto)
    except ExamHubException as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())

@router.delete("/{question_id}")
def delete_question(question_id: str, user: TokenData = Depends(require_teacher)):
    try:
        QuestionService.delete_question(question_id)
        return {"message": "Question removed successfully."}
    except ExamHubException as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())
