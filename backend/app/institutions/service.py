"""
ExamHub - Institution Application Service
Business logic for managing departments, faculties, and student enrollment cohorts.
"""

from typing import List, Dict, Any
from backend.app.institutions.repository import InstitutionRepository
from backend.app.institutions.schemas import DepartmentResponse

class InstitutionService:
    """Service layer managing departments and institutional hierarchies."""

    @staticmethod
    def get_all_departments() -> List[DepartmentResponse]:
        raw = InstitutionRepository.list_departments()
        return [DepartmentResponse(**r) for r in raw]

    @staticmethod
    def add_department(name: str, code: str, desc: str, head: str) -> str:
        return InstitutionRepository.create_department(name, code, desc, head)
