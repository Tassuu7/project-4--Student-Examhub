"""
ExamHub - Automated Tests for Subject Management
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
    seed_database(force_reseed=True)

def get_token(username: str) -> str:
    res = client.post("/api/v1/auth/login", json={"username_or_email": username, "password": "password123"})
    return res.json()["access_token"]

def test_list_subjects():
    token = get_token("student_alice")
    res = client.get("/api/v1/subjects", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert "items" in data
    assert len(data["items"]) >= 4

def test_create_subject_as_admin():
    token = get_token("admin")
    res = client.post(
        "/api/v1/subjects",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "code": "MATH101",
            "name": "Calculus & Linear Algebra",
            "description": "Foundational mathematics for computing",
            "department": "Mathematics"
        }
    )
    assert res.status_code == 200
    data = res.json()
    assert data["code"] == "MATH101"
    assert data["name"] == "Calculus & Linear Algebra"

def test_teacher_cannot_create_subject():
    token = get_token("teacher_smith")
    res = client.post(
        "/api/v1/subjects",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "code": "BIO101",
            "name": "General Biology",
            "department": "Sciences"
        }
    )
    assert res.status_code == 403

def test_duplicate_subject_code_fails():
    token = get_token("admin")
    res = client.post(
        "/api/v1/subjects",
        headers={"Authorization": f"Bearer {token}"},
        json={"code": "CS101", "name": "Duplicate Computer Science"}
    )
    assert res.status_code in [400, 422]
