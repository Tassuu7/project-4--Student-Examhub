"""
ExamHub - Automated Tests for Authentication & Token Security
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database.schema import init_db
from backend.app.database.seeder import seed_database
from backend.app.core.security import hash_password, verify_password, generate_token, verify_token

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    init_db()
    seed_database()

def test_password_hashing():
    raw_pass = "SecureSecret123!"
    hashed = hash_password(raw_pass)
    assert hashed != raw_pass
    assert ":" in hashed
    assert verify_password(raw_pass, hashed) is True
    assert verify_password("WrongPassword", hashed) is False

def test_token_generation_and_verification():
    payload = {"sub": "user-123", "role": "teacher", "username": "prof_x"}
    token = generate_token(payload, expires_in_seconds=60)
    assert token is not None
    verified = verify_token(token)
    assert verified is not None
    assert verified["sub"] == "user-123"
    assert verified["role"] == "teacher"

def test_expired_token():
    payload = {"sub": "user-expired"}
    token = generate_token(payload, expires_in_seconds=-10)
    verified = verify_token(token)
    assert verified is None

def test_valid_admin_login():
    response = client.post(
        "/api/v1/auth/login",
        json={"username_or_email": "admin", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["role"] == "admin"
    assert data["user"]["username"] == "admin"

def test_valid_teacher_login():
    response = client.post(
        "/api/v1/auth/login",
        json={"username_or_email": "teacher_smith", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["role"] == "teacher"
    assert data["user"]["teacher_code"] == "TCH001"

def test_valid_student_login():
    response = client.post(
        "/api/v1/auth/login",
        json={"username_or_email": "student_alice", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["role"] == "student"
    assert data["user"]["student_code"] == "STU001"

def test_invalid_login_credentials():
    response = client.post(
        "/api/v1/auth/login",
        json={"username_or_email": "admin", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    err = response.json()
    assert "error" in err or "detail" in err

def test_get_current_user_profile():
    # Login as student
    login_res = client.post(
        "/api/v1/auth/login",
        json={"username_or_email": "student_alice", "password": "password123"}
    )
    token = login_res.json()["access_token"]
    
    # Get profile
    res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    prof = res.json()
    assert prof["username"] == "student_alice"
    assert prof["role"] == "student"

def test_unauthorized_access_without_token():
    res = client.get("/api/v1/auth/me")
    assert res.status_code == 401
