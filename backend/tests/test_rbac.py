"""
ExamHub - Automated Tests for Role-Based Access Control (RBAC)
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database.schema import init_db
from backend.app.database.seeder import seed_database

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    init_db()
    seed_database()

def get_token_for(username: str) -> str:
    res = client.post(
        "/api/v1/auth/login",
        json={"username_or_email": username, "password": "password123"}
    )
    assert res.status_code == 200
    return res.json()["access_token"]

def test_admin_can_access_user_list():
    admin_token = get_token_for("admin")
    res = client.get("/api/v1/users", headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 200
    data = res.json()
    assert "items" in data
    assert len(data["items"]) > 0

def test_teacher_forbidden_from_admin_user_list():
    teacher_token = get_token_for("teacher_smith")
    res = client.get("/api/v1/users", headers={"Authorization": f"Bearer {teacher_token}"})
    assert res.status_code == 403

def test_student_forbidden_from_admin_user_list():
    student_token = get_token_for("student_alice")
    res = client.get("/api/v1/users", headers={"Authorization": f"Bearer {student_token}"})
    assert res.status_code == 403
