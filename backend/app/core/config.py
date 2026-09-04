"""
ExamHub - Core Configuration Settings
Proprietary Examination Management Platform
"""

import os
from pathlib import Path
from typing import List, Optional

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True, parents=True)

DATABASE_PATH = os.environ.get("EXAMHUB_DB_PATH", str(DATA_DIR / "examhub.sqlite3"))
SECRET_KEY = os.environ.get("EXAMHUB_SECRET_KEY", "examhub-production-system-security-key-2026-strict")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("EXAMHUB_TOKEN_EXPIRE_MINUTES", "720"))
SESSION_TIMEOUT_MINUTES = int(os.environ.get("EXAMHUB_SESSION_TIMEOUT", "60"))
CORS_ORIGINS: List[str] = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "*"
]

PROJECT_NAME = "ExamHub - Student Examination Management System"
VERSION = "1.0.0"
API_PREFIX = "/api/v1"
DEBUG = os.environ.get("DEBUG", "False").lower() in ("1", "true")

# Examination Engine Rules
DEFAULT_PASSING_PERCENTAGE = 40.0
AUTOSAVE_INTERVAL_SECONDS = 15
TIMER_GRACE_PERIOD_SECONDS = 10
MAX_OPTIONS_PER_QUESTION = 4
MIN_OPTIONS_PER_QUESTION = 2
DEFAULT_MARKS_PER_QUESTION = 1.0
MAX_QUESTION_MARKS = 100.0

# Password Policy Configuration
MIN_PASSWORD_LENGTH = 6
MAX_PASSWORD_LENGTH = 128
REQUIRE_DIGIT = False
REQUIRE_SPECIAL_CHAR = False
PASSWORD_SALT = "examhub_crypto_salt_v1_secure"
