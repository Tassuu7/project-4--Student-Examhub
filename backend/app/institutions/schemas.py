"""
ExamHub - Academic Institutions, Departments, and Cohort Schemas
Contracts for multi-department organizations, academic terms, and courses.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class DepartmentCreate(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    head_of_department: Optional[str] = None

class DepartmentResponse(BaseModel):
    id: str
    name: str
    code: str
    description: Optional[str] = None
    head_of_department: Optional[str] = None
    total_subjects: int
    total_teachers: int
    created_at: str

class AcademicCohortCreate(BaseModel):
    name: str
    department_id: str
    term_name: str  # e.g., Fall 2026, Spring 2026
    start_date: str
    end_date: str

class AcademicCohortResponse(BaseModel):
    id: str
    name: str
    department_id: str
    department_name: str
    term_name: str
    start_date: str
    end_date: str
    student_count: int
    created_at: str
