"""
ExamHub - Automated Tests for Question Bank System
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database.schema import init_db
from backend.app.database.seeder import seed_database
from backend.app.subjects.repository import SubjectRepository

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    init_db()
    seed_database()

def get_token(username: str) -> str:
    res = client.post("/api/v1/auth/login", json={"username_or_email": username, "password": "password123"})
    return res.json()["access_token"]

def test_list_questions_with_filtering():
    token = get_token("teacher_smith")
    # List all
    res = client.get("/api/v1/questions", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert len(data["items"]) > 0

    # Filter by difficulty
    res_easy = client.get("/api/v1/questions?difficulty=Easy", headers={"Authorization": f"Bearer {token}"})
    assert res_easy.status_code == 200
    for q in res_easy.json()["items"]:
        assert q["difficulty"] == "Easy"

def test_create_question_as_teacher():
    token = get_token("teacher_smith")
    sub = SubjectRepository.get_by_code("CS101")
    assert sub is not None

    res = client.post(
        "/api/v1/questions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "subject_id": sub["id"],
            "question_text": "What is the output of len([1, 2, 3, 4]) in Python?",
            "option_a": "3",
            "option_b": "4",
            "option_c": "5",
            "option_d": "Error",
            "correct_answer": "B",
            "marks": 1.0,
            "difficulty": "Easy",
            "topic": "Built-in Functions",
            "explanation": "len() returns the number of items of an iterable or collection."
        }
    )
    assert res.status_code == 200
    created = res.json()
    assert created["correct_answer"] == "B"
    assert created["marks"] == 1.0
    assert created["topic"] == "Built-in Functions"

def test_student_cannot_create_question():
    token = get_token("student_alice")
    sub = SubjectRepository.get_by_code("CS101")

    res = client.post(
        "/api/v1/questions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "subject_id": sub["id"],
            "question_text": "Unauthorized student question attempt",
            "option_a": "A", "option_b": "B", "option_c": "C", "option_d": "D",
            "correct_answer": "A", "marks": 1.0
        }
    )
    assert res.status_code == 403

def test_csv_template_and_export():
    token = get_token("teacher_smith")
    # Template
    res_tmpl = client.get("/api/v1/questions/template.csv", headers={"Authorization": f"Bearer {token}"})
    assert res_tmpl.status_code == 200
    assert "SubjectCode,QuestionText" in res_tmpl.text

    # Export
    res_exp = client.get("/api/v1/questions/export.csv", headers={"Authorization": f"Bearer {token}"})
    assert res_exp.status_code == 200
    assert "CS101" in res_exp.text
