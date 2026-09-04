"""
ExamHub - Institution & Department Repository Layer
Manages academic faculties, departments, and course cohorts.
"""

from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime
from backend.app.database.connection import get_db_connection

class InstitutionRepository:
    """Persistence operations for departments and academic cohorts."""

    @staticmethod
    def ensure_tables():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS departments (
                id TEXT PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                code TEXT UNIQUE NOT NULL,
                description TEXT,
                head_of_department TEXT,
                created_at TEXT NOT NULL
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS academic_cohorts (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                department_id TEXT NOT NULL,
                term_name TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE
            );
        """)
        conn.commit()

    @staticmethod
    def list_departments() -> List[Dict[str, Any]]:
        InstitutionRepository.ensure_tables()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT d.*,
                   (SELECT COUNT(*) FROM subjects s WHERE s.department = d.name) as total_subjects,
                   (SELECT COUNT(*) FROM teachers t WHERE t.department = d.name) as total_teachers
            FROM departments d
            ORDER BY d.name ASC
        """)
        return [dict(r) for r in cursor.fetchall()]

    @staticmethod
    def create_department(name: str, code: str, desc: Optional[str], head: Optional[str]) -> str:
        InstitutionRepository.ensure_tables()
        conn = get_db_connection()
        cursor = conn.cursor()
        dept_id = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO departments (id, name, code, description, head_of_department, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (dept_id, name, code, desc or "", head or "", datetime.utcnow().isoformat()))
        conn.commit()
        return dept_id
