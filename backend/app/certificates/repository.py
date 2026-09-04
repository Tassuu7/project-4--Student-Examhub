"""
ExamHub - Certificate Repository Layer
Manages persistence, retrieval, status updates, and lookup for issued credentials.
"""

from typing import Optional, List, Dict, Any
from backend.app.database.connection import get_db_connection

class CertificateRepository:
    """Database access methods for certificates and digital academic credentials."""

    @staticmethod
    def ensure_table():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS certificates (
                id TEXT PRIMARY KEY,
                certificate_code TEXT UNIQUE NOT NULL,
                attempt_id TEXT UNIQUE NOT NULL,
                exam_id TEXT NOT NULL,
                student_id TEXT NOT NULL,
                title TEXT NOT NULL,
                issue_date TEXT NOT NULL,
                expiry_date TEXT,
                verification_hash TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'expired', 'revoked')),
                revocation_reason TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (attempt_id) REFERENCES exam_attempts(id) ON DELETE CASCADE,
                FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
            );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cert_code ON certificates(certificate_code);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cert_student ON certificates(student_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cert_attempt ON certificates(attempt_id);")
        conn.commit()

    @staticmethod
    def create_certificate(data: Dict[str, Any]) -> str:
        CertificateRepository.ensure_table()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO certificates (
                id, certificate_code, attempt_id, exam_id, student_id,
                title, issue_date, expiry_date, verification_hash,
                status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["id"], data["certificate_code"], data["attempt_id"],
            data["exam_id"], data["student_id"], data["title"],
            data["issue_date"], data.get("expiry_date"),
            data["verification_hash"], data.get("status", "active"),
            data["created_at"]
        ))
        conn.commit()
        return data["id"]

    @staticmethod
    def get_by_code(code: str) -> Optional[Dict[str, Any]]:
        CertificateRepository.ensure_table()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.*, u.full_name as student_name, st.student_id_code as roll_number,
                   e.name as exam_name, s.code as subject_code, s.name as subject_name,
                   r.percentage, r.grade
            FROM certificates c
            JOIN students st ON c.student_id = st.id
            JOIN users u ON st.user_id = u.id
            JOIN exams e ON c.exam_id = e.id
            JOIN subjects s ON e.subject_id = s.id
            JOIN results r ON c.attempt_id = r.attempt_id
            WHERE c.certificate_code = ?
        """, (code,))
        row = cursor.fetchone()
        return dict(row) if row else None

    @staticmethod
    def get_by_attempt_id(attempt_id: str) -> Optional[Dict[str, Any]]:
        CertificateRepository.ensure_table()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.*, u.full_name as student_name, st.student_id_code as roll_number,
                   e.name as exam_name, s.code as subject_code, s.name as subject_name,
                   r.percentage, r.grade
            FROM certificates c
            JOIN students st ON c.student_id = st.id
            JOIN users u ON st.user_id = u.id
            JOIN exams e ON c.exam_id = e.id
            JOIN subjects s ON e.subject_id = s.id
            JOIN results r ON c.attempt_id = r.attempt_id
            WHERE c.attempt_id = ?
        """, (attempt_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    @staticmethod
    def get_student_certificates(student_id: str) -> List[Dict[str, Any]]:
        CertificateRepository.ensure_table()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.*, u.full_name as student_name, st.student_id_code as roll_number,
                   e.name as exam_name, s.code as subject_code, s.name as subject_name,
                   r.percentage, r.grade
            FROM certificates c
            JOIN students st ON c.student_id = st.id
            JOIN users u ON st.user_id = u.id
            JOIN exams e ON c.exam_id = e.id
            JOIN subjects s ON e.subject_id = s.id
            JOIN results r ON c.attempt_id = r.attempt_id
            WHERE c.student_id = ?
            ORDER BY c.issue_date DESC
        """, (student_id,))
        return [dict(r) for r in cursor.fetchall()]

    @staticmethod
    def revoke_certificate(code: str, reason: str) -> bool:
        CertificateRepository.ensure_table()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE certificates
            SET status = 'revoked', revocation_reason = ?
            WHERE certificate_code = ?
        """, (reason, code))
        conn.commit()
        return cursor.rowcount > 0
