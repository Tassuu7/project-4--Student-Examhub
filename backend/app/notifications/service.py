"""
ExamHub - Notifications Application Service
Handles in-app notification delivery, broadcast messaging, and read status updates.
"""

from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime
from backend.app.database.connection import get_db_connection
from backend.app.notifications.schemas import NotificationItem

class NotificationService:
    """Operations for user alert messaging."""

    @staticmethod
    def send_notification(user_id: str, title: str, message: str, ntype: str = "info", link: Optional[str] = None) -> str:
        conn = get_db_connection()
        cursor = conn.cursor()
        nid = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO notifications (id, user_id, title, message, type, is_read, link, created_at)
            VALUES (?, ?, ?, ?, ?, 0, ?, ?)
        """, (nid, user_id, title, message, ntype, link or "", datetime.utcnow().isoformat()))
        conn.commit()
        return nid

    @staticmethod
    def broadcast_to_role(role: Optional[str], title: str, message: str, ntype: str = "announcement") -> int:
        conn = get_db_connection()
        cursor = conn.cursor()

        if role and role in ("student", "teacher", "admin"):
            cursor.execute("SELECT id FROM users WHERE role = ? AND is_active = 1", (role,))
        else:
            cursor.execute("SELECT id FROM users WHERE is_active = 1")

        user_ids = [r[0] for r in cursor.fetchall()]
        now = datetime.utcnow().isoformat()
        for uid in user_ids:
            nid = str(uuid.uuid4())
            cursor.execute("""
                INSERT INTO notifications (id, user_id, title, message, type, is_read, link, created_at)
                VALUES (?, ?, ?, ?, ?, 0, '', ?)
            """, (nid, uid, title, message, ntype, now))

        conn.commit()
        return len(user_ids)

    @staticmethod
    def get_user_notifications(user_id: str) -> List[NotificationItem]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, user_id, title, message, type, is_read, link, created_at
            FROM notifications
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 50
        """, (user_id,))
        rows = [dict(r) for r in cursor.fetchall()]
        return [
            NotificationItem(
                id=r["id"],
                user_id=r["user_id"],
                title=r["title"],
                message=r["message"],
                type=r["type"],
                is_read=bool(r["is_read"]),
                link=r.get("link"),
                created_at=r["created_at"]
            ) for r in rows
        ]

    @staticmethod
    def mark_as_read(notification_id: str, user_id: str) -> bool:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE notifications SET is_read = 1 WHERE id = ? AND user_id = ?", (notification_id, user_id))
        conn.commit()
        return cursor.rowcount > 0
