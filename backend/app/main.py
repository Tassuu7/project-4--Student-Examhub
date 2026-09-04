"""
ExamHub - FastAPI Application Entry Point
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.app.core.config import PROJECT_NAME, VERSION, API_PREFIX, CORS_ORIGINS
from backend.app.core.exceptions import ExamHubException
from backend.app.database.schema import init_db
from backend.app.database.seeder import seed_database
from backend.app.auth.router import router as auth_router
from backend.app.users.router import router as users_router
from backend.app.subjects.router import router as subjects_router
from backend.app.questions.router import router as questions_router
from backend.app.exams.router import router as exams_router
from backend.app.analytics.router import router as analytics_router
from backend.app.certificates.router import router as certificates_router
from backend.app.proctoring.router import router as proctoring_router
from backend.app.grading.router import router as grading_router
from backend.app.export_import.router import router as export_import_router
from backend.app.audit.router import router as audit_router
from backend.app.institutions.router import router as institutions_router
from backend.app.notifications.router import router as notifications_router
from backend.app.adaptive_testing.router import router as adaptive_testing_router
from backend.app.qti.router import router as qti_router
from backend.app.rubrics.router import router as rubrics_router
from backend.app.plagiarism.router import router as plagiarism_router
from backend.app.accreditation.router import router as accreditation_router
from backend.app.biometrics.router import router as biometrics_router
from backend.app.question_engines.router import router as question_engines_router
from backend.app.reporting.router import router as reporting_router
from backend.app.tenancy.router import router as tenancy_router
from backend.app.notifications_engine.router import router as notifications_engine_router
from backend.app.analytics_drilldown.router import router as analytics_drilldown_router
from backend.app.audit_compliance.router import router as audit_compliance_router
from backend.app.exam_delivery.router import router as exam_delivery_router
from backend.app.feedbacks.router import router as feedbacks_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure database schema and seed fixtures exist
    init_db()
    seed_database()
    yield
    # Shutdown: Clean resources if needed

app = FastAPI(
    title=PROJECT_NAME,
    version=VERSION,
    lifespan=lifespan,
    docs_url=f"{API_PREFIX}/docs",
    openapi_url=f"{API_PREFIX}/openapi.json"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler for custom domain exceptions
@app.exception_handler(ExamHubException)
async def examhub_exception_handler(request: Request, exc: ExamHubException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict()
    )

# Health Check
@app.get("/api/health")
@app.get(f"{API_PREFIX}/health")
def health_check():
    return {
        "status": "healthy",
        "service": PROJECT_NAME,
        "version": VERSION,
        "database": "sqlite3:connected"
    }

# Mount core routers
app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(users_router, prefix=API_PREFIX)
app.include_router(subjects_router, prefix=API_PREFIX)
app.include_router(questions_router, prefix=API_PREFIX)
app.include_router(exams_router, prefix=API_PREFIX)
app.include_router(analytics_router, prefix=API_PREFIX)
app.include_router(certificates_router, prefix=API_PREFIX)
app.include_router(proctoring_router, prefix=API_PREFIX)
app.include_router(grading_router, prefix=API_PREFIX)
app.include_router(export_import_router, prefix=API_PREFIX)
app.include_router(audit_router, prefix=API_PREFIX)
app.include_router(institutions_router, prefix=API_PREFIX)
app.include_router(notifications_router, prefix=API_PREFIX)
app.include_router(feedbacks_router, prefix=API_PREFIX)
app.include_router(adaptive_testing_router)
app.include_router(qti_router)
app.include_router(rubrics_router)
app.include_router(plagiarism_router)
app.include_router(accreditation_router)
app.include_router(biometrics_router)
app.include_router(question_engines_router)
app.include_router(reporting_router)
app.include_router(tenancy_router)
app.include_router(notifications_engine_router)
app.include_router(analytics_drilldown_router)
app.include_router(audit_compliance_router)
app.include_router(exam_delivery_router)

if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PORT", os.environ.get("EXAMHUB_PORT", "8001")))
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=port, reload=True)
