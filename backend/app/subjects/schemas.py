"""
ExamHub - Subject Schemas & DTOs
"""

from typing import Optional, List
from pydantic import BaseModel, Field

class SubjectCreateRequest(BaseModel):
    code: str = Field(..., min_length=2, max_length=20, description="Unique subject code e.g. CS101")
    name: str = Field(..., min_length=2, max_length=150, description="Subject full title")
    description: Optional[str] = Field(None, max_length=1000)
    department: Optional[str] = Field(None, max_length=100)

class SubjectUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=150)
    description: Optional[str] = Field(None, max_length=1000)
    department: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None

class TeacherAssignmentDTO(BaseModel):
    teacher_id: str
    teacher_name: str
    teacher_code: str
    department: Optional[str] = None
    assigned_at: str

class SubjectResponse(BaseModel):
    id: str
    code: str
    name: str
    description: Optional[str] = None
    department: Optional[str] = None
    is_active: bool
    question_count: int = 0
    exam_count: int = 0
    assigned_teachers: List[TeacherAssignmentDTO] = []
    created_at: str
    updated_at: str

class AssignTeacherRequest(BaseModel):
    teacher_id: str
