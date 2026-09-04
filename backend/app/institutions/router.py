"""
ExamHub - Institution & Department API Router
Exposes endpoints for listing and creating academic departments.
"""

from fastapi import APIRouter, Depends
from typing import List, Dict, Any

from backend.app.auth.rbac import require_role
from backend.app.institutions.schemas import DepartmentResponse, DepartmentCreate
from backend.app.institutions.service import InstitutionService

router = APIRouter(prefix="/institutions", tags=["Institutions & Departments"])

@router.get("/departments", response_model=List[DepartmentResponse])
def get_departments(
    current_user: Dict[str, Any] = Depends(require_role(["admin", "teacher"]))
):
    """Retrieve all academic departments with subject and faculty metrics."""
    return InstitutionService.get_all_departments()

@router.post("/departments")
def create_department(
    payload: DepartmentCreate,
    current_user: Dict[str, Any] = Depends(require_role(["admin"]))
):
    """Admin-only endpoint: Register a new academic department."""
    dept_id = InstitutionService.add_department(
        payload.name, payload.code, payload.description or "", payload.head_of_department or ""
    )
    return {"id": dept_id, "status": "created"}
