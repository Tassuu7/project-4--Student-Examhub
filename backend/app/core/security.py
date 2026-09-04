"""
ExamHub - Cryptographic & Authentication Utilities
PBKDF2-HMAC-SHA256 password hashing & secure token generation
"""

import hashlib
import hmac
import base64
import json
import time
import secrets
from typing import Optional, Dict, Any
from backend.app.core.config import SECRET_KEY, PASSWORD_SALT

def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        (salt + PASSWORD_SALT).encode('utf-8'),
        iterations=100_000
    )
    return f"{salt}:{dk.hex()}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        parts = hashed_password.split(':')
        if len(parts) != 2:
            return False
        salt, stored_hash = parts[0], parts[1]
        dk = hashlib.pbkdf2_hmac(
            'sha256',
            plain_password.encode('utf-8'),
            (salt + PASSWORD_SALT).encode('utf-8'),
            iterations=100_000
        )
        return hmac.compare_digest(dk.hex(), stored_hash)
    except Exception:
        return False

def generate_token(payload: Dict[str, Any], expires_in_seconds: int = 43200) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    body = payload.copy()
    now = int(time.time())
    body["iat"] = now
    body["exp"] = now + expires_in_seconds
    
    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode('utf-8')).decode('utf-8').rstrip('=')
    body_b64 = base64.urlsafe_b64encode(json.dumps(body).encode('utf-8')).decode('utf-8').rstrip('=')
    
    signing_input = f"{header_b64}.{body_b64}"
    signature = hmac.new(
        SECRET_KEY.encode('utf-8'),
        signing_input.encode('utf-8'),
        hashlib.sha256
    ).digest()
    sig_b64 = base64.urlsafe_b64encode(signature).decode('utf-8').rstrip('=')
    
    return f"{header_b64}.{body_b64}.{sig_b64}"

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        header_b64, body_b64, sig_b64 = parts
        
        signing_input = f"{header_b64}.{body_b64}"
        expected_sig = hmac.new(
            SECRET_KEY.encode('utf-8'),
            signing_input.encode('utf-8'),
            hashlib.sha256
        ).digest()
        expected_sig_b64 = base64.urlsafe_b64encode(expected_sig).decode('utf-8').rstrip('=')
        
        if not hmac.compare_digest(sig_b64, expected_sig_b64):
            return None
            
        rem = len(body_b64) % 4
        padded_b64 = body_b64 + ('=' * (4 - rem) if rem else '')
        payload = json.loads(base64.urlsafe_b64decode(padded_b64).decode('utf-8'))
        
        # Check expiration
        now = int(time.time())
        if "exp" in payload and payload["exp"] < now:
            return None
            
        return payload
    except Exception:
        return None
