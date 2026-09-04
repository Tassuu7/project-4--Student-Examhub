"""
Unit & Integration Tests for ExamHub Exam Engine
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database.seeder import seed_database
from backend.app.database.schema import init_db
from backend.app.subjects.repository import SubjectRepository

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    init_db()
    seed_database()

def get_token(username):
    res = client.post(
        "/api/v1/auth/login",
        json={"username_or_email": username, "password": "password123"}
    )
    assert res.status_code == 200, f"Login failed for {username}: {res.text}"
    return res.json()["access_token"]

def test_full_exam_lifecycle():
    teacher_token = get_token("teacher_smith")
    student_token = get_token("student_carol")
    t_headers = {"Authorization": f"Bearer {teacher_token}"}
    s_headers = {"Authorization": f"Bearer {student_token}"}

    # 1. Fetch subjects and questions
    sub_res = client.get("/api/v1/subjects", headers=t_headers)
    assert sub_res.status_code == 200
    subjects = sub_res.json()["items"]
    assert len(subjects) > 0
    subject_id = subjects[0]["id"]

    q_res = client.get(f"/api/v1/questions?subject_id={subject_id}", headers=t_headers)
    assert q_res.status_code == 200
    questions = q_res.json()["items"]
    assert len(questions) >= 2
    q1 = questions[0]
    q2 = questions[1]

    # Fetch students
    stu_res = client.get("/api/v1/users/students", headers=t_headers)
    assert stu_res.status_code == 200
    students = stu_res.json()["items"]
    assert len(students) > 0
    # Carol's student id
    student_record = next(s for s in students if "carol" in s["email"])
    student_id = student_record["student_id"]

    # 2. Teacher creates an exam
    create_payload = {
        "name": "Mid-Term CS Assessment",
        "subject_id": subject_id,
        "description": "Comprehensive Mid-Term examination",
        "duration_minutes": 30,
        "passing_percentage": 50.0,
        "start_date": "2026-09-01T00:00:00Z",
        "end_date": "2026-09-30T23:59:59Z",
        "instructions": "No external aids allowed. All questions mandatory.",
        "question_ids": [q1["id"], q2["id"]],
        "student_ids": [student_id]
    }
    create_res = client.post("/api/v1/exams", json=create_payload, headers=t_headers)
    assert create_res.status_code == 201, create_res.text
    exam_id = create_res.json()["exam_id"]

    # 3. Activate exam
    status_res = client.put(f"/api/v1/exams/{exam_id}/status", json={"status": "active"}, headers=t_headers)
    assert status_res.status_code == 200

    # 4. Student checks portal
    portal_res = client.get("/api/v1/exams/student/portal", headers=s_headers)
    assert portal_res.status_code == 200
    portal_exams = portal_res.json()["items"]
    my_exam = next((e for e in portal_exams if e["id"] == exam_id), None)
    assert my_exam is not None
    assert my_exam["status"] == "active"

    # 5. Student starts attempt
    start_res = client.post(f"/api/v1/exams/{exam_id}/attempt/start", headers=s_headers)
    assert start_res.status_code == 200
    attempt_data = start_res.json()
    attempt_id = attempt_data["attempt_id"]
    assert len(attempt_data["questions"]) == 2
    # Ensure correct answers are NOT leaked to student during active attempt
    for pub_q in attempt_data["questions"]:
        assert "correct_answer" not in pub_q
        assert "explanation" not in pub_q

    # 6. Student logs proctoring event (e.g. tab switch)
    proc_res = client.post(
        f"/api/v1/exams/attempt/{attempt_id}/proctoring",
        json={"event_type": "tab_switch", "details": "Switched to tab 2"},
        headers=s_headers
    )
    assert proc_res.status_code == 200

    # 7. Student answers question 1 correctly, question 2 incorrectly
    ans1_res = client.post(
        f"/api/v1/exams/attempt/{attempt_id}/answer",
        json={"question_id": q1["id"], "selected_option": q1["correct_answer"], "is_marked_for_review": False},
        headers=s_headers
    )
    assert ans1_res.status_code == 200

    wrong_opt = "A" if q2["correct_answer"] != "A" else "B"
    ans2_res = client.post(
        f"/api/v1/exams/attempt/{attempt_id}/answer",
        json={"question_id": q2["id"], "selected_option": wrong_opt, "is_marked_for_review": True},
        headers=s_headers
    )
    assert ans2_res.status_code == 200

    # 8. Student submits attempt
    submit_res = client.post(f"/api/v1/exams/attempt/{attempt_id}/submit", headers=s_headers)
    assert submit_res.status_code == 200
    result = submit_res.json()

    assert result["total_questions"] == 2
    assert result["correct_count"] == 1
    assert result["wrong_count"] == 1
    assert result["percentage"] == 50.0
    assert result["pass_fail"] == "PASS"

    # 9. Student views their result
    view_res = client.get(f"/api/v1/exams/attempt/{attempt_id}/result", headers=s_headers)
    assert view_res.status_code == 200
    assert view_res.json()["attempt_id"] == attempt_id

    # 10. Teacher checks exam results and proctoring integrity
    t_res = client.get(f"/api/v1/exams/{exam_id}/results", headers=t_headers)
    assert t_res.status_code == 200
    assert len(t_res.json()["items"]) == 1

    t_integ = client.get(f"/api/v1/exams/attempt/{attempt_id}/integrity", headers=t_headers)
    assert t_integ.status_code == 200
    assert t_integ.json()["total_events"] == 1

def test_auto_generate_exam():
    teacher_token = get_token("teacher_smith")
    t_headers = {"Authorization": f"Bearer {teacher_token}"}

    sub_res = client.get("/api/v1/subjects", headers=t_headers)
    subject_id = sub_res.json()["items"][0]["id"]

    req = {
        "subject_id": subject_id,
        "name": "Auto-Generated Quick Quiz",
        "duration_minutes": 20,
        "passing_percentage": 40.0,
        "start_date": "2026-09-01T00:00:00Z",
        "end_date": "2026-09-30T23:59:59Z",
        "easy_count": 1,
        "medium_count": 1,
        "hard_count": 0
    }
    gen_res = client.post("/api/v1/exams/auto-generate", json=req, headers=t_headers)
    assert gen_res.status_code == 201
    assert "exam_id" in gen_res.json()
