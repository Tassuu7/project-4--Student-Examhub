"""
ExamHub - Question Bank Business Service
"""

from typing import Optional, List, Dict, Any
from backend.app.questions.repository import QuestionRepository
from backend.app.subjects.repository import SubjectRepository
from backend.app.questions.schemas import QuestionCreateRequest, QuestionUpdateRequest, QuestionResponse, BulkImportSummary
from backend.app.questions.bulk_importer import QuestionBulkService
from backend.app.core.constants import QuestionDifficulty
from backend.app.core.exceptions import ValidationError, ResourceNotFoundError
from backend.app.core.pagination import PaginationParams, PaginatedResponse

class QuestionService:
    @staticmethod
    def create_question(dto: QuestionCreateRequest, teacher_id: Optional[str] = None) -> QuestionResponse:
        subject = SubjectRepository.get_by_id(dto.subject_id)
        if not subject:
            raise ResourceNotFoundError("Subject", dto.subject_id)

        qid = QuestionRepository.create_question({
            "subject_id": dto.subject_id,
            "teacher_id": teacher_id,
            "question_text": dto.question_text,
            "option_a": dto.option_a,
            "option_b": dto.option_b,
            "option_c": dto.option_c,
            "option_d": dto.option_d,
            "correct_answer": dto.correct_answer.value,
            "marks": dto.marks,
            "difficulty": dto.difficulty.value,
            "topic": dto.topic,
            "explanation": dto.explanation
        })
        return QuestionService.get_question(qid)

    @staticmethod
    def update_question(question_id: str, dto: QuestionUpdateRequest) -> QuestionResponse:
        existing = QuestionRepository.get_by_id(question_id)
        if not existing:
            raise ResourceNotFoundError("Question", question_id)

        if dto.subject_id:
            subject = SubjectRepository.get_by_id(dto.subject_id)
            if not subject:
                raise ResourceNotFoundError("Subject", dto.subject_id)

        update_data = dto.model_dump(exclude_unset=True)
        if "correct_answer" in update_data and update_data["correct_answer"]:
            update_data["correct_answer"] = dto.correct_answer.value
        if "difficulty" in update_data and update_data["difficulty"]:
            update_data["difficulty"] = dto.difficulty.value

        QuestionRepository.update_question(question_id, update_data)
        return QuestionService.get_question(question_id)

    @staticmethod
    def get_question(question_id: str) -> QuestionResponse:
        raw = QuestionRepository.get_by_id(question_id)
        if not raw:
            raise ResourceNotFoundError("Question", question_id)

        return QuestionResponse(
            id=raw["id"],
            subject_id=raw["subject_id"],
            subject_code=raw["subject_code"],
            subject_name=raw["subject_name"],
            teacher_id=raw.get("teacher_id"),
            teacher_name=raw.get("teacher_name"),
            question_text=raw["question_text"],
            option_a=raw["option_a"],
            option_b=raw["option_b"],
            option_c=raw["option_c"],
            option_d=raw["option_d"],
            correct_answer=raw["correct_answer"],
            marks=float(raw["marks"]),
            difficulty=raw["difficulty"],
            topic=raw.get("topic"),
            explanation=raw.get("explanation"),
            is_active=bool(raw["is_active"]),
            used_in_exam_count=raw.get("used_in_exam_count", 0),
            created_at=raw["created_at"],
            updated_at=raw["updated_at"]
        )

    @staticmethod
    def delete_question(question_id: str):
        existing = QuestionRepository.get_by_id(question_id)
        if not existing:
            raise ResourceNotFoundError("Question", question_id)
        QuestionRepository.delete_question(question_id)

    @staticmethod
    def list_questions(
        subject_id: Optional[str],
        difficulty: Optional[QuestionDifficulty],
        topic: Optional[str],
        search: Optional[str],
        teacher_id: Optional[str],
        params: PaginationParams
    ) -> PaginatedResponse[QuestionResponse]:
        items_raw, total = QuestionRepository.list_questions(
            subject_id=subject_id,
            difficulty=difficulty,
            topic=topic,
            search=search,
            teacher_id=teacher_id,
            is_active=True,
            offset=params.offset,
            limit=params.limit
        )
        items = [
            QuestionResponse(
                id=r["id"],
                subject_id=r["subject_id"],
                subject_code=r["subject_code"],
                subject_name=r["subject_name"],
                teacher_id=r.get("teacher_id"),
                teacher_name=r.get("teacher_name"),
                question_text=r["question_text"],
                option_a=r["option_a"],
                option_b=r["option_b"],
                option_c=r["option_c"],
                option_d=r["option_d"],
                correct_answer=r["correct_answer"],
                marks=float(r["marks"]),
                difficulty=r["difficulty"],
                topic=r.get("topic"),
                explanation=r.get("explanation"),
                is_active=bool(r["is_active"]),
                used_in_exam_count=r.get("used_in_exam_count", 0),
                created_at=r["created_at"],
                updated_at=r["updated_at"]
            )
            for r in items_raw
        ]
        return PaginatedResponse.create(items, total, params)

    @staticmethod
    def import_from_csv(csv_content: str, teacher_id: Optional[str] = None) -> BulkImportSummary:
        return QuestionBulkService.import_questions_from_csv(csv_content, teacher_id)

    @staticmethod
    def export_to_csv(subject_id: Optional[str] = None) -> str:
        return QuestionBulkService.export_questions_to_csv(subject_id)

    @staticmethod
    def get_csv_template() -> str:
        return QuestionBulkService.generate_csv_template()
