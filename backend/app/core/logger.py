"""
ExamHub - System Logger and Activity Audit Logger
"""

import logging
import sys
import datetime
from typing import Optional, Dict, Any

logger = logging.getLogger("examhub")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def log_audit_event(user_id: Optional[str], action: str, entity_type: str, entity_id: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    msg = f"AUDIT: user={user_id or 'anonymous'} action={action} entity={entity_type} id={entity_id or '-'} details={details or {}}"
    logger.info(msg)
