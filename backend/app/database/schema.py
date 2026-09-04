"""
ExamHub - Relational Database Schema DDL Definition
Creates tables, constraints, foreign keys, and indexes for SQLite
"""

from backend.app.database.connection import get_db_connection
from backend.app.core.logger import logger

DDL_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('admin', 'teacher', 'student')),
        is_active INTEGER NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
    CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
    CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
    """,
    """
    CREATE TABLE IF NOT EXISTS students (
        id TEXT PRIMARY KEY,
        user_id TEXT UNIQUE NOT NULL,
        student_id_code TEXT UNIQUE NOT NULL,
        grade_level TEXT,
        department TEXT,
        phone TEXT,
        guardian_contact TEXT,
        enrolled_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_students_code ON students(student_id_code);
    CREATE INDEX IF NOT EXISTS idx_students_user ON students(user_id);
    """,
    """
    CREATE TABLE IF NOT EXISTS teachers (
        id TEXT PRIMARY KEY,
        user_id TEXT UNIQUE NOT NULL,
        teacher_id_code TEXT UNIQUE NOT NULL,
        department TEXT,
        qualification TEXT,
        specialization TEXT,
        hired_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_teachers_code ON teachers(teacher_id_code);
    CREATE INDEX IF NOT EXISTS idx_teachers_user ON teachers(user_id);
    """,
    """
    CREATE TABLE IF NOT EXISTS subjects (
        id TEXT PRIMARY KEY,
        code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        department TEXT,
        is_active INTEGER NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_subjects_code ON subjects(code);
    CREATE INDEX IF NOT EXISTS idx_subjects_active ON subjects(is_active);
    """,
    """
    CREATE TABLE IF NOT EXISTS subject_teachers (
        id TEXT PRIMARY KEY,
        subject_id TEXT NOT NULL,
        teacher_id TEXT NOT NULL,
        assigned_at TEXT NOT NULL,
        UNIQUE(subject_id, teacher_id),
        FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
        FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS questions (
        id TEXT PRIMARY KEY,
        subject_id TEXT NOT NULL,
        teacher_id TEXT,
        question_text TEXT NOT NULL,
        option_a TEXT NOT NULL,
        option_b TEXT NOT NULL,
        option_c TEXT NOT NULL,
        option_d TEXT NOT NULL,
        correct_answer TEXT NOT NULL CHECK(correct_answer IN ('A', 'B', 'C', 'D')),
        marks REAL NOT NULL DEFAULT 1.0,
        difficulty TEXT NOT NULL CHECK(difficulty IN ('Easy', 'Medium', 'Hard')),
        topic TEXT,
        explanation TEXT,
        is_active INTEGER NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
        FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE SET NULL
    );
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_questions_subject ON questions(subject_id);
    CREATE INDEX IF NOT EXISTS idx_questions_teacher ON questions(teacher_id);
    CREATE INDEX IF NOT EXISTS idx_questions_difficulty ON questions(difficulty);
    CREATE INDEX IF NOT EXISTS idx_questions_topic ON questions(topic);
    """,
    """
    CREATE TABLE IF NOT EXISTS exams (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        subject_id TEXT NOT NULL,
        teacher_id TEXT NOT NULL,
        description TEXT,
        duration_minutes INTEGER NOT NULL,
        total_marks REAL NOT NULL DEFAULT 0.0,
        passing_percentage REAL NOT NULL DEFAULT 40.0,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        instructions TEXT,
        status TEXT NOT NULL CHECK(status IN ('draft', 'scheduled', 'active', 'completed', 'cancelled')),
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
        FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE
    );
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_exams_subject ON exams(subject_id);
    CREATE INDEX IF NOT EXISTS idx_exams_teacher ON exams(teacher_id);
    CREATE INDEX IF NOT EXISTS idx_exams_status ON exams(status);
    """,
    """
    CREATE TABLE IF NOT EXISTS exam_questions (
        id TEXT PRIMARY KEY,
        exam_id TEXT NOT NULL,
        question_id TEXT NOT NULL,
        order_index INTEGER NOT NULL,
        marks_allocated REAL NOT NULL DEFAULT 1.0,
        UNIQUE(exam_id, question_id),
        FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE,
        FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
    );
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_exam_questions_exam ON exam_questions(exam_id);
    """,
    """
    CREATE TABLE IF NOT EXISTS exam_assignments (
        id TEXT PRIMARY KEY,
        exam_id TEXT NOT NULL,
        student_id TEXT NOT NULL,
        assigned_at TEXT NOT NULL,
        can_attempt INTEGER NOT NULL DEFAULT 1,
        attempts_allowed INTEGER NOT NULL DEFAULT 1,
        UNIQUE(exam_id, student_id),
        FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE,
        FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
    );
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_assignments_exam ON exam_assignments(exam_id);
    CREATE INDEX IF NOT EXISTS idx_assignments_student ON exam_assignments(student_id);
    """,
    """
    CREATE TABLE IF NOT EXISTS exam_attempts (
        id TEXT PRIMARY KEY,
        exam_id TEXT NOT NULL,
        student_id TEXT NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT,
        time_remaining_seconds INTEGER NOT NULL,
        status TEXT NOT NULL CHECK(status IN ('not_started', 'in_progress', 'submitted', 'auto_submitted', 'evaluated', 'expired')),
        total_score REAL DEFAULT 0.0,
        percentage REAL DEFAULT 0.0,
        grade TEXT,
        result TEXT CHECK(result IN ('PASS', 'FAIL', NULL)),
        evaluated_at TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE,
        FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
    );
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_attempts_exam ON exam_attempts(exam_id);
    CREATE INDEX IF NOT EXISTS idx_attempts_student ON exam_attempts(student_id);
    CREATE INDEX IF NOT EXISTS idx_attempts_status ON exam_attempts(status);
    """,
    """
    CREATE TABLE IF NOT EXISTS student_answers (
        id TEXT PRIMARY KEY,
        attempt_id TEXT NOT NULL,
        question_id TEXT NOT NULL,
        selected_option TEXT CHECK(selected_option IN ('A', 'B', 'C', 'D', NULL)),
        is_correct INTEGER DEFAULT 0,
        marks_obtained REAL DEFAULT 0.0,
        is_marked_for_review INTEGER NOT NULL DEFAULT 0,
        saved_at TEXT NOT NULL,
        UNIQUE(attempt_id, question_id),
        FOREIGN KEY (attempt_id) REFERENCES exam_attempts(id) ON DELETE CASCADE,
        FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
    );
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_student_answers_attempt ON student_answers(attempt_id);
    """,
    """
    CREATE TABLE IF NOT EXISTS results (
        id TEXT PRIMARY KEY,
        attempt_id TEXT UNIQUE NOT NULL,
        exam_id TEXT NOT NULL,
        student_id TEXT NOT NULL,
        total_questions INTEGER NOT NULL,
        correct_count INTEGER NOT NULL,
        wrong_count INTEGER NOT NULL,
        unanswered_count INTEGER NOT NULL,
        total_marks REAL NOT NULL,
        obtained_marks REAL NOT NULL,
        percentage REAL NOT NULL,
        grade TEXT NOT NULL,
        pass_fail TEXT NOT NULL CHECK(pass_fail IN ('PASS', 'FAIL')),
        rank INTEGER,
        generated_at TEXT NOT NULL,
        FOREIGN KEY (attempt_id) REFERENCES exam_attempts(id) ON DELETE CASCADE,
        FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE,
        FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
    );
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_results_exam ON results(exam_id);
    CREATE INDEX IF NOT EXISTS idx_results_student ON results(student_id);
    CREATE INDEX IF NOT EXISTS idx_results_pass_fail ON results(pass_fail);
    """,
    """
    CREATE TABLE IF NOT EXISTS notifications (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        type TEXT NOT NULL,
        is_read INTEGER NOT NULL DEFAULT 0,
        link TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id);
    CREATE INDEX IF NOT EXISTS idx_notifications_read ON notifications(is_read);
    """,
    """
    CREATE TABLE IF NOT EXISTS audit_logs (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        action TEXT NOT NULL,
        entity_type TEXT NOT NULL,
        entity_id TEXT,
        details_json TEXT,
        created_at TEXT NOT NULL
    );
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_logs(user_id);
    CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_logs(created_at);
    """,
    """
    CREATE TABLE IF NOT EXISTS proctoring_logs (
        id TEXT PRIMARY KEY,
        attempt_id TEXT NOT NULL,
        event_type TEXT NOT NULL,
        details TEXT,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (attempt_id) REFERENCES exam_attempts(id) ON DELETE CASCADE
    );
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_proctoring_attempt ON proctoring_logs(attempt_id);
    """
]

def init_db():
    """Execute DDL statements to set up SQLite schema."""
    conn = get_db_connection()
    cursor = conn.cursor()
    for stmt in DDL_STATEMENTS:
        cursor.executescript(stmt)
    conn.commit()
    logger.info("Database schema initialized successfully.")

if __name__ == "__main__":
    init_db()
