"""
ExamHub - SQLite Database Connection & Transaction Manager
Thread-safe connection pooling, SQLite WAL mode, foreign key enforcement
"""

import sqlite3
import threading
from contextlib import contextmanager
from typing import Generator, Any, List, Dict, Optional
from backend.app.core.config import DATABASE_PATH
from backend.app.core.logger import logger

_local = threading.local()

def get_db_connection() -> sqlite3.Connection:
    """Obtain or initialize thread-local SQLite connection with proper PRAGMAs."""
    if not hasattr(_local, "connection") or _local.connection is None:
        conn = sqlite3.connect(DATABASE_PATH, timeout=30.0, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        # Enable Foreign Keys and Write-Ahead Logging for high concurrency
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        conn.execute("PRAGMA busy_timeout = 10000;")
        _local.connection = conn
    return _local.connection

@contextmanager
def transaction() -> Generator[sqlite3.Connection, None, None]:
    """Provide a transactional scope around a series of operations."""
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(f"Transaction rollback due to error: {e}")
        raise

def dict_from_row(row: Optional[sqlite3.Row]) -> Optional[Dict[str, Any]]:
    """Convert an sqlite3.Row to a plain dictionary."""
    if row is None:
        return None
    return dict(row)

def list_from_rows(rows: List[sqlite3.Row]) -> List[Dict[str, Any]]:
    """Convert a list of sqlite3.Rows to plain dictionaries."""
    return [dict(r) for r in rows]
