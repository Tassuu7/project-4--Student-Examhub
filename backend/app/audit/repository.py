"""
ExamHub - Audit Repository Layer
Provides tamper-evident append-only querying of administrative actions.
"""

from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime
from backend.app.database.connection import get_db_connection

class AuditRepository:
    """Manages audit trail queries and record append operations."""

    @staticmethod
    def record_action(user_id: Optional[str], action: str, entity_type: str, entity_id: Optional[str], details: Optional[str] = None) -> str:
        conn = get_db_connection()
        cursor = conn.cursor()
        log_id = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO audit_logs (id, user_id, action, entity_type, entity_id, details_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (log_id, user_id, action, entity_type, entity_id, details or "{}", datetime.utcnow().isoformat()))
        conn.commit()
        return log_id

    @staticmethod
    def get_logs(limit: int = 100, action: Optional[str] = None, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT al.id, al.user_id, al.action, al.entity_type, al.entity_id,
                   al.details_json, al.created_at, u.username
            FROM audit_logs al
            LEFT JOIN users u ON al.user_id = u.id
            WHERE 1=1
        """
        params = []
        if action:
            query += " AND al.action = ?"
            params.append(action)
        if user_id:
            query += " AND al.user_id = ?"
            params.append(user_id)

        query += " ORDER BY al.created_at DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        return [dict(r) for r in cursor.fetchall()]
