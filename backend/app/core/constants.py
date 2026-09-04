"""
ExamHub - System Constants and Enums
"""

from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"

class ExamStatus(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class AttemptStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    AUTO_SUBMITTED = "auto_submitted"
    EVALUATED = "evaluated"
    EXPIRED = "expired"

class QuestionDifficulty(str, Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

class CorrectOption(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"

class QuestionType(str, Enum):
    MCQ_SINGLE = "mcq_single"
    MCQ_MULTIPLE = "mcq_multiple"
    TRUE_FALSE = "true_false"

class EvaluationResult(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"

class NotificationType(str, Enum):
    EXAM_SCHEDULED = "exam_scheduled"
    EXAM_REMINDER = "exam_reminder"
    RESULT_AVAILABLE = "result_available"
    SUBMISSION_SUCCESS = "submission_success"
    SYSTEM_ALERT = "system_alert"

# Grading Scale Standard:
# 90-100 = A+
# 80-89  = A
# 70-79  = B
# 60-69  = C
# 50-59  = D
# 40-49  = E
# Below 40 = F
GRADE_SCALE = [
    {"min": 90.0, "max": 100.0, "grade": "A+", "description": "Outstanding"},
    {"min": 80.0, "max": 89.99, "grade": "A", "description": "Excellent"},
    {"min": 70.0, "max": 79.99, "grade": "B", "description": "Very Good"},
    {"min": 60.0, "max": 69.99, "grade": "C", "description": "Good"},
    {"min": 50.0, "max": 59.99, "grade": "D", "description": "Satisfactory"},
    {"min": 40.0, "max": 49.99, "grade": "E", "description": "Pass"},
    {"min": 0.0, "max": 39.99, "grade": "F", "description": "Fail"},
]
