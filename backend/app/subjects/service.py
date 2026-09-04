"""
ExamHub - Subject Business Service
"""

from typing import Optional, List, Dict, Any
from backend.app.subjects.repository import SubjectRepository
from backend.app.subjects.schemas import SubjectCreateRequest, SubjectUpdateRequest, SubjectResponse, TeacherAssignmentDTO
from backend.app.core.exceptions import ValidationError, ResourceNotFoundError
from backend.app.core.pagination import PaginationParams, PaginatedResponse

class SubjectService:
    @staticmethod
    def create_subject(dto: SubjectCreateRequest) -> SubjectResponse:
        existing = SubjectRepository.get_by_code(dto.code)
        if existing:
            raise ValidationError(f"Subject with code '{dto.code.upper()}' already exists.")

        sub_id = SubjectRepository.create_subject(dto.model_dump())
        return SubjectService.get_subject(sub_id)

    @staticmethod
    def update_subject(subject_id: str, dto: SubjectUpdateRequest) -> SubjectResponse:
        existing = SubjectRepository.get_by_id(subject_id)
        if not existing:
            raise ResourceNotFoundError("Subject", subject_id)

        SubjectRepository.update_subject(subject_id, dto.model_dump(exclude_unset=True))
        return SubjectService.get_subject(subject_id)

    @staticmethod
    def get_subject(subject_id: str) -> SubjectResponse:
        raw = SubjectRepository.get_by_id(subject_id)
        if not raw:
            raise ResourceNotFoundError("Subject", subject_id)

        teachers_raw = SubjectRepository.get_assigned_teachers(subject_id)
        assigned_teachers = [
            TeacherAssignmentDTO(
                teacher_id=t["teacher_id"],
                teacher_name=t["teacher_name"],
                teacher_code=t["teacher_code"],
                department=t.get("department"),
                assigned_at=t["assigned_at"]
            )
            for t in teachers_raw
        ]

        return SubjectResponse(
            id=raw["id"],
            code=raw["code"],
            name=raw["name"],
            description=raw.get("description"),
            department=raw.get("department"),
            is_active=bool(raw["is_active"]),
            question_count=raw.get("question_count", 0),
            exam_count=raw.get("exam_count", 0),
            assigned_teachers=assigned_teachers,
            created_at=raw["created_at"],
            updated_at=raw["updated_at"]
        )

    @staticmethod
    def list_subjects(search: Optional[str], department: Optional[str],
                      is_active: Optional[bool], teacher_id: Optional[str],
                      params: PaginationParams) -> PaginatedResponse[SubjectResponse]:
        items_raw, total = SubjectRepository.list_subjects(
            search=search, department=department, is_active=is_active,
            teacher_id=teacher_id, offset=params.offset, limit=params.limit
        )
        items = []
        for r in items_raw:
            teachers_raw = SubjectRepository.get_assigned_teachers(r["id"])
            assigned_teachers = [
                TeacherAssignmentDTO(
                    teacher_id=t["teacher_id"],
                    teacher_name=t["teacher_name"],
                    teacher_code=t["teacher_code"],
                    department=t.get("department"),
                    assigned_at=t["assigned_at"]
                )
                for t in teachers_raw
            ]
            items.append(
                SubjectResponse(
                    id=r["id"],
                    code=r["code"],
                    name=r["name"],
                    description=r.get("description"),
                    department=r.get("department"),
                    is_active=bool(r["is_active"]),
                    question_count=r.get("question_count", 0),
                    exam_count=r.get("exam_count", 0),
                    assigned_teachers=assigned_teachers,
                    created_at=r["created_at"],
                    updated_at=r["updated_at"]
                )
            )
        return PaginatedResponse.create(items, total, params)

    @staticmethod
    def assign_teacher_to_subject(subject_id: str, teacher_id: str):
        existing = SubjectRepository.get_by_id(subject_id)
        if not existing:
            raise ResourceNotFoundError("Subject", subject_id)
        SubjectRepository.assign_teacher(subject_id, teacher_id)

    @staticmethod
    def remove_teacher_from_subject(subject_id: str, teacher_id: str):
        existing = SubjectRepository.get_by_id(subject_id)
        if not existing:
            raise ResourceNotFoundError("Subject", subject_id)
        SubjectRepository.remove_teacher(subject_id, teacher_id)
