"""
ExamHub - Domain and HTTP Exception Definitions
"""

from typing import Optional, Any, Dict

class ExamHubException(Exception):
    def __init__(self, message: str, code: str = "GENERIC_ERROR", status_code: int = 400, details: Optional[Any] = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details

    def to_dict(self) -> Dict[str, Any]:
        res = {"error": self.message, "code": self.code}
        if self.details is not None:
            res["details"] = self.details
        return res

class AuthenticationError(ExamHubException):
    def __init__(self, message: str = "Invalid credentials", details: Optional[Any] = None):
        super().__init__(message=message, code="AUTHENTICATION_FAILED", status_code=401, details=details)

class AuthorizationError(ExamHubException):
    def __init__(self, message: str = "Access denied: insufficient permissions", details: Optional[Any] = None):
        super().__init__(message=message, code="PERMISSION_DENIED", status_code=403, details=details)

class ResourceNotFoundError(ExamHubException):
    def __init__(self, resource: str, identifier: Any):
        super().__init__(
            message=f"{resource} with identifier '{identifier}' was not found",
            code="RESOURCE_NOT_FOUND",
            status_code=404,
            details={"resource": resource, "id": identifier}
        )

class ValidationError(ExamHubException):
    def __init__(self, message: str, field_errors: Optional[Dict[str, str]] = None):
        super().__init__(
            message=message,
            code="VALIDATION_FAILED",
            status_code=422,
            details=field_errors or {}
        )

class ExamUnavailableError(ExamHubException):
    def __init__(self, message: str = "Exam is not currently available for attendance"):
        super().__init__(message=message, code="EXAM_UNAVAILABLE", status_code=400)

class ExamAlreadySubmittedError(ExamHubException):
    def __init__(self, message: str = "Exam attempt has already been submitted and locked"):
        super().__init__(message=message, code="EXAM_ALREADY_SUBMITTED", status_code=409)

class ExamTimeExpiredError(ExamHubException):
    def __init__(self, message: str = "Exam time limit has expired"):
        super().__init__(message=message, code="EXAM_TIME_EXPIRED", status_code=400)

class NotFoundException(ExamHubException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message=message, code="RESOURCE_NOT_FOUND", status_code=404)

class ValidationException(ExamHubException):
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message=message, code="VALIDATION_FAILED", status_code=422)

