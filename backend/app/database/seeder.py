"""
ExamHub - Synthetic Demo Data Seeder
Populates users, teachers, students, subjects, questions, exams, attempts, results, and notifications.
No real data; 100% synthetic educational demonstration fixtures.
"""

import uuid
import datetime
import hashlib
from backend.app.database.connection import get_db_connection, transaction
from backend.app.core.security import hash_password
from backend.app.core.constants import UserRole, ExamStatus, AttemptStatus, QuestionDifficulty
from backend.app.core.logger import logger

def seed_database(force_reseed: bool = False):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM users;")
    user_count = cursor.fetchone()[0]
    if user_count > 0 and not force_reseed:
        logger.info("Database already seeded. Skipping initial seeding.")
        return

    if force_reseed and user_count > 0:
        tables = [
            "audit_logs", "notifications", "certificates", "student_feedbacks",
            "results", "student_answers", "exam_attempts", "exam_assignments",
            "exam_questions", "exams", "questions", "subject_teachers",
            "subjects", "students", "teachers", "users"
        ]
        for t in tables:
            try:
                cursor.execute(f"DELETE FROM {t};")
            except Exception:
                pass

    logger.info("Starting synthetic database population...")
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    yesterday = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)).isoformat()
    two_days_ago = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=2)).isoformat()
    tomorrow = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)).isoformat()
    next_week = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)).isoformat()
    next_year = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365)).isoformat()
    
    default_pass = hash_password("password123")

    with transaction():
        # 1. PRINCIPAL & ADMIN USERS
        admin_id = str(uuid.uuid4())
        principal_id = str(uuid.uuid4())
        cursor.execute(
            """INSERT INTO users (id, username, email, password_hash, full_name, role, is_active, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?);""",
            (admin_id, "admin", "admin@examhub.edu", default_pass, "System Administrator", UserRole.ADMIN.value, now, now)
        )
        cursor.execute(
            """INSERT INTO users (id, username, email, password_hash, full_name, role, is_active, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?);""",
            (principal_id, "principal_sharma", "principal@examhub.edu", default_pass, "Dr. Ramesh Sharma (Principal)", UserRole.ADMIN.value, now, now)
        )

        # 2. TEACHERS
        teachers_data = [
            ("teacher_smith", "smith@examhub.edu", "Prof. Robert Smith", "TCH001", "Computer Science", "Ph.D. in Computer Science", "Algorithms & Systems"),
            ("teacher_chen", "chen@examhub.edu", "Dr. Angela Chen", "TCH002", "Data Science", "Ph.D. in Applied Mathematics", "Machine Learning & Stats"),
            ("teacher_patel", "patel@examhub.edu", "Prof. Rajesh Patel", "TCH003", "Software Engineering", "M.Tech in Software Systems", "Web Architecture & Cloud"),
        ]
        teacher_records = []
        for uname, email, fname, tcode, dept, qual, spec in teachers_data:
            uid = str(uuid.uuid4())
            tid = str(uuid.uuid4())
            cursor.execute(
                """INSERT INTO users (id, username, email, password_hash, full_name, role, is_active, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?);""",
                (uid, uname, email, default_pass, fname, UserRole.TEACHER.value, now, now)
            )
            cursor.execute(
                """INSERT INTO teachers (id, user_id, teacher_id_code, department, qualification, specialization, hired_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?);""",
                (tid, uid, tcode, dept, qual, spec, two_days_ago)
            )
            teacher_records.append({"user_id": uid, "teacher_id": tid, "name": fname, "username": uname})

        # 3. SYNTHETIC STUDENTS COHORT
        students_data = [
            ("student_alice", "alice@examhub.edu", "Alice Walker", "STU001", "Senior", "Computer Science", "+1-555-0101"),
            ("student_bob", "bob@examhub.edu", "Bob Miller", "STU002", "Junior", "Computer Science", "+1-555-0102"),
            ("student_david", "david@examhub.edu", "David Kim", "STU004", "Sophomore", "Software Engineering", "+1-555-0104"),
            ("student_eva", "eva@examhub.edu", "Eva Green", "STU005", "Junior", "Computer Science", "+1-555-0105"),
            ("student_frank", "frank@examhub.edu", "Frank Wright", "STU006", "Freshman", "Computer Science", "+1-555-0106"),
            ("student_grace", "grace@examhub.edu", "Grace Hopper", "STU007", "Senior", "Computer Science", "+1-555-0107"),
            ("student_henry", "henry@examhub.edu", "Henry Ford", "STU008", "Sophomore", "Software Engineering", "+1-555-0108"),
        ]
        student_records = []
        for uname, email, fname, scode, grade, dept, phone in students_data:
            uid = str(uuid.uuid4())
            sid = str(uuid.uuid4())
            cursor.execute(
                """INSERT INTO users (id, username, email, password_hash, full_name, role, is_active, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?);""",
                (uid, uname, email, default_pass, fname, UserRole.STUDENT.value, now, now)
            )
            cursor.execute(
                """INSERT INTO students (id, user_id, student_id_code, grade_level, department, phone, guardian_contact, enrolled_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?);""",
                (sid, uid, scode, grade, dept, phone, "guardian@example.com", two_days_ago)
            )
            student_records.append({"user_id": uid, "student_id": sid, "name": fname, "username": uname, "code": scode})

        # 4. SUBJECTS
        subjects_data = [
            ("CS101", "Python Programming", "Fundamentals of Python, data structures, and procedural programming", "Computer Science"),
            ("CS201", "Data Structures & Algorithms", "Linear and non-linear data structures, searching, sorting, and asymptotic analysis", "Computer Science"),
            ("SE301", "Software Engineering Principles", "Software development lifecycle, design patterns, testing, and agile methodologies", "Software Engineering"),
            ("DS202", "Database Management Systems", "Relational database concepts, SQL queries, normalization, and ACID properties", "Data Science"),
        ]
        subject_records = []
        for code, name, desc, dept in subjects_data:
            sub_id = str(uuid.uuid4())
            cursor.execute(
                """INSERT INTO subjects (id, code, name, description, department, is_active, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, 1, ?, ?);""",
                (sub_id, code, name, desc, dept, two_days_ago, now)
            )
            subject_records.append({"id": sub_id, "code": code, "name": name})

        # Assign Teachers to Subjects
        for idx, sub in enumerate(subject_records):
            t_rec = teacher_records[idx % len(teacher_records)]
            cursor.execute(
                """INSERT INTO subject_teachers (id, subject_id, teacher_id, assigned_at)
                   VALUES (?, ?, ?, ?);""",
                (str(uuid.uuid4()), sub["id"], t_rec["teacher_id"], two_days_ago)
            )

        # 5. QUESTIONS FOR EACH SUBJECT
        questions_pool = [
            # Python Programming (CS101)
            (
                "CS101",
                "Which data type is immutable in Python?",
                "List", "Dictionary", "Set", "Tuple", "D",
                1.0, "Easy", "Data Types",
                "Tuples cannot be modified after instantiation in Python."
            ),
            (
                "CS101",
                "What is the output of bool('False') in Python?",
                "False", "True", "None", "SyntaxError", "B",
                1.0, "Easy", "Data Types",
                "Any non-empty string in Python evaluates to True in boolean context."
            ),
            (
                "CS101",
                "Which built-in module is used for regular expressions in Python?",
                "regex", "pyregex", "re", "string", "C",
                1.0, "Easy", "Standard Library",
                "The 're' module provides full regular expression matching operations."
            ),
            (
                "CS101",
                "How is memory managed in Python?",
                "Manual allocation only", "Garbage collection & reference counting", "Static compilation", "Stack allocation only", "B",
                2.0, "Medium", "Memory Management",
                "Python uses reference counting along with a cyclic garbage collector."
            ),
            (
                "CS101",
                "What does the '__init__' method represent in Python classes?",
                "Class destructor", "Static constructor", "Instance initializer", "Package entry point", "C",
                1.0, "Easy", "Object-Oriented Programming",
                "The __init__ method is called when an instance of a class is created."
            ),
            (
                "CS101",
                "What will be the result of: [x**2 for x in range(5) if x % 2 == 0]?",
                "[0, 4, 16]", "[1, 9, 25]", "[0, 1, 4, 9, 16]", "[4, 16]", "A",
                2.0, "Medium", "List Comprehensions",
                "The even numbers in range(5) are 0, 2, 4. Their squares are 0, 4, 16."
            ),
            (
                "CS101",
                "Which keyword is used to create an anonymous function in Python?",
                "def", "func", "lambda", "inline", "C",
                1.0, "Easy", "Functions",
                "lambda allows creating small anonymous functions in Python."
            ),
            (
                "CS101",
                "What is the time complexity of looking up a key in a standard Python dictionary?",
                "O(n)", "O(1) average", "O(log n)", "O(n^2)", "B",
                2.0, "Medium", "Data Structures",
                "Python dictionaries are implemented as hash tables with O(1) average lookup."
            ),
            (
                "CS101",
                "What is the purpose of the 'with' statement in Python?",
                "Loop iteration", "Context management and resource cleanup", "Exception suppression", "Thread locking only", "B",
                2.0, "Medium", "Context Managers",
                "The with statement guarantees cleanup of resources via __enter__ and __exit__."
            ),
            (
                "CS101",
                "What is GIL in the CPython implementation?",
                "Global Interface Link", "General Instruction Loop", "Global Interpreter Lock", "Graphics Integration Layer", "C",
                3.0, "Hard", "CPython Internals",
                "The GIL is a mutex that protects access to Python objects, preventing multiple threads from executing Python bytecodes at once."
            ),
            # Data Structures & Algorithms (CS201)
            (
                "CS201",
                "What is the worst-case time complexity of QuickSort?",
                "O(n log n)", "O(n)", "O(n^2)", "O(log n)", "C",
                2.0, "Medium", "Sorting Algorithms",
                "Worst case occurs when the chosen pivot is always the smallest or largest element, leading to O(n^2)."
            ),
            (
                "CS201",
                "Which data structure operates on a Last-In, First-Out (LIFO) principle?",
                "Queue", "Priority Queue", "Stack", "Linked List", "C",
                1.0, "Easy", "Linear Data Structures",
                "A stack adds and removes elements from the top, following LIFO."
            ),
            (
                "CS201",
                "What is the height of a balanced binary search tree containing n nodes?",
                "O(1)", "O(log n)", "O(n)", "O(n log n)", "B",
                2.0, "Medium", "Tree Structures",
                "Balanced BSTs like AVL or Red-Black trees maintain a height bounded by O(log n)."
            ),
            (
                "CS201",
                "Dijkstra's algorithm is used for which problem?",
                "Minimum Spanning Tree", "Single-source shortest path", "Topological sorting", "Maximum network flow", "B",
                2.0, "Medium", "Graph Algorithms",
                "Dijkstra calculates shortest paths from a source to all vertices in a weighted graph with non-negative weights."
            ),
            (
                "CS201",
                "What is the best average-case search complexity in a sorted array of size n?",
                "O(n)", "O(log n)", "O(1)", "O(n log n)", "B",
                1.0, "Easy", "Searching",
                "Binary search repeatedly divides the search interval in half, taking O(log n)."
            ),
            # Database Management Systems (DS202)
            (
                "DS202",
                "Which SQL clause is used to filter group aggregations?",
                "WHERE", "ORDER BY", "HAVING", "GROUP BY", "C",
                1.0, "Easy", "SQL Queries",
                "HAVING filters records after aggregation, whereas WHERE filters before."
            ),
            (
                "DS202",
                "What does ACID stand for in database transaction management?",
                "Atomicity, Consistency, Isolation, Durability",
                "Accuracy, Control, Integrity, Data",
                "Automatic, Concurrent, Indexed, Distributed",
                "Access, Concurrency, Isolation, Durability",
                "A",
                2.0, "Medium", "Transactions",
                "ACID ensures transactions are processed reliably in relational database systems."
            ),
            (
                "DS202",
                "Which normal form eliminates transitive dependencies?",
                "1NF", "2NF", "3NF", "BCNF", "C",
                2.0, "Medium", "Normalization",
                "3NF requires that no non-prime attribute is transitively dependent on any candidate key."
            ),
            (
                "DS202",
                "What type of join returns all rows from the left table and matched rows from the right?",
                "INNER JOIN", "LEFT OUTER JOIN", "RIGHT OUTER JOIN", "CROSS JOIN", "B",
                1.0, "Easy", "SQL Joins",
                "A LEFT JOIN returns all records from the left table and matched rows from the right table."
            ),
            # Software Engineering Principles (SE301)
            (
                "SE301",
                "Which design pattern restricts the instantiation of a class to one single object?",
                "Factory Pattern", "Observer Pattern", "Singleton Pattern", "Strategy Pattern", "C",
                1.0, "Easy", "Design Patterns",
                "Singleton ensures a class has only one instance and provides a global access point to it."
            ),
            (
                "SE301",
                "What does CI/CD stand for in modern DevOps practices?",
                "Code Integration / Code Deployment",
                "Continuous Integration / Continuous Delivery (or Deployment)",
                "Centralized Infrastructure / Cloud Delivery",
                "Component Isolation / Continuous Debugging",
                "B",
                1.0, "Easy", "DevOps & Quality",
                "CI/CD automates the integration, testing, and deployment of code changes."
            ),
        ]

        # Map subjects by code
        sub_map = {s["code"]: s["id"] for s in subject_records}
        tch_id = teacher_records[0]["teacher_id"]

        question_records = []
        for item in questions_pool:
            sub_code, qtext, oa, ob, oc, od, ans, marks, diff, topic, expl = item
            qid = str(uuid.uuid4())
            cursor.execute(
                """INSERT INTO questions (id, subject_id, teacher_id, question_text, option_a, option_b, option_c, option_d,
                                          correct_answer, marks, difficulty, topic, explanation, is_active, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?);""",
                (qid, sub_map[sub_code], tch_id, qtext, oa, ob, oc, od, ans, marks, diff, topic, expl, two_days_ago, now)
            )
            question_records.append({
                "id": qid, "sub_code": sub_code, "subject_id": sub_map[sub_code], "marks": marks, "ans": ans, "qtext": qtext
            })

        # 6. EXAMS
        # Exam 1: Active Python Programming Midterm (CS101)
        exam1_id = str(uuid.uuid4())
        cursor.execute(
            """INSERT INTO exams (id, name, subject_id, teacher_id, description, duration_minutes, total_marks,
                                 passing_percentage, start_date, end_date, instructions, status, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
            (
                exam1_id,
                "Python Programming Midterm Assessment",
                sub_map["CS101"],
                tch_id,
                "Comprehensive evaluation of core Python syntax, collections, memory management, and functions.",
                30,
                15.0,
                40.0,
                yesterday,
                next_week,
                "1. Answer all questions.\n2. You can navigate between questions freely.\n3. Exam will automatically submit when time expires.\n4. Do not refresh or close your browser.",
                ExamStatus.ACTIVE.value,
                two_days_ago,
                now
            )
        )

        # Attach 8 questions to Exam 1
        py_questions = [q for q in question_records if q["sub_code"] == "CS101"]
        for idx, q in enumerate(py_questions[:8]):
            cursor.execute(
                """INSERT INTO exam_questions (id, exam_id, question_id, order_index, marks_allocated)
                   VALUES (?, ?, ?, ?, ?);""",
                (str(uuid.uuid4()), exam1_id, q["id"], idx + 1, q["marks"])
            )

        # Assign all students to Exam 1
        for s in student_records:
            cursor.execute(
                """INSERT INTO exam_assignments (id, exam_id, student_id, assigned_at, can_attempt, attempts_allowed)
                   VALUES (?, ?, ?, ?, 1, 1);""",
                (str(uuid.uuid4()), exam1_id, s["student_id"], two_days_ago)
            )

        # Exam 2: Completed Data Structures Quiz
        exam2_id = str(uuid.uuid4())
        cursor.execute(
            """INSERT INTO exams (id, name, subject_id, teacher_id, description, duration_minutes, total_marks,
                                 passing_percentage, start_date, end_date, instructions, status, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
            (
                exam2_id,
                "Data Structures Fundamentals Quiz",
                sub_map["CS201"],
                teacher_records[1]["teacher_id"],
                "Assessment covering stacks, queues, trees, and search algorithms.",
                20,
                8.0,
                50.0,
                two_days_ago,
                yesterday,
                "Timed quiz. Read every question carefully before answering.",
                ExamStatus.COMPLETED.value,
                two_days_ago,
                yesterday
            )
        )
        ds_questions = [q for q in question_records if q["sub_code"] == "CS201"]
        for idx, q in enumerate(ds_questions):
            cursor.execute(
                """INSERT INTO exam_questions (id, exam_id, question_id, order_index, marks_allocated)
                   VALUES (?, ?, ?, ?, ?);""",
                (str(uuid.uuid4()), exam2_id, q["id"], idx + 1, q["marks"])
            )

        # Exam 3: DBMS & SQL Proficiency Examination (DS202)
        exam3_id = str(uuid.uuid4())
        cursor.execute(
            """INSERT INTO exams (id, name, subject_id, teacher_id, description, duration_minutes, total_marks,
                                 passing_percentage, start_date, end_date, instructions, status, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
            (
                exam3_id,
                "DBMS & SQL Proficiency Examination",
                sub_map["DS202"],
                teacher_records[2]["teacher_id"],
                "Covers SQL querying, relational algebra, ACID transactions, and database normalization.",
                45,
                6.0,
                40.0,
                two_days_ago,
                next_week,
                "Please review SQL aggregation and joins prior to beginning.",
                ExamStatus.ACTIVE.value,
                two_days_ago,
                now
            )
        )
        db_questions = [q for q in question_records if q["sub_code"] == "DS202"]
        for idx, q in enumerate(db_questions):
            cursor.execute(
                """INSERT INTO exam_questions (id, exam_id, question_id, order_index, marks_allocated)
                   VALUES (?, ?, ?, ?, ?);""",
                (str(uuid.uuid4()), exam3_id, q["id"], idx + 1, q["marks"])
            )

        for s in student_records:
            cursor.execute(
                """INSERT INTO exam_assignments (id, exam_id, student_id, assigned_at, can_attempt, attempts_allowed)
                   VALUES (?, ?, ?, ?, 1, 1);""",
                (str(uuid.uuid4()), exam3_id, s["student_id"], two_days_ago)
            )

        # 7. SEED COMPLETED ATTEMPTS, RESULTS, CERTIFICATES & FEEDBACK FOR STUDENTS
        from backend.app.certificates.repository import CertificateRepository
        CertificateRepository.ensure_table()

        # Student performances across Exam 2 (Data Structures)
        perf_data = [
            # (student_index, correct_count, score, percentage, grade, pass_fail, rank, feedback_text, rating, has_cert, cert_code)
            (0, 4, 7.0, 87.5, "A", "PASS", 2, "Outstanding work, Alice! Exceptional grasp of algorithm optimization and space-time complexity analysis.", 5, True, "CERT-2026-DS-001"),
            (1, 3, 5.0, 62.5, "C", "PASS", 4, "Good demonstration of core data structure concepts. Review recursion edge cases and balance factors.", 4, False, None),
            (2, 3, 4.5, 56.2, "D", "PASS", 5, "Satisfactory completion. Focus on mastering pointer arithmetic and tree rebalancing operations.", 3, False, None),
            (3, 2, 3.5, 43.8, "D", "PASS", 6, "Passed the baseline threshold. Extra practice with hash tables and linked lists recommended.", 3, False, None),
            (4, 1, 2.0, 25.0, "F", "FAIL", 7, "Academic intervention needed. Fundamental concepts require guided practice. Please attend office hours.", 2, False, None),
            (5, 4, 8.0, 100.0, "A+", "PASS", 1, "Flawless score! Exemplary mastery of data structures, complexity bounds, and algorithm implementation.", 5, True, "CERT-2026-DS-002"),
            (6, 3, 5.5, 68.8, "C", "PASS", 3, "Solid effort. Good understanding of stack and queue implementations. Keep developing tree traversal skills.", 4, False, None),
        ]

        for s_idx, cor, score, pct, grd, res, rnk, fb_text, fb_rating, has_cert, ccode in perf_data:
            if s_idx >= len(student_records):
                continue
            s = student_records[s_idx]
            att_id = str(uuid.uuid4())
            
            cursor.execute(
                """INSERT INTO exam_attempts (id, exam_id, student_id, start_time, end_time, time_remaining_seconds,
                                             status, total_score, percentage, grade, result, evaluated_at, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, 0, ?, ?, ?, ?, ?, ?, ?, ?);""",
                (att_id, exam2_id, s["student_id"], two_days_ago, yesterday, AttemptStatus.EVALUATED.value,
                 score, pct, grd, res, yesterday, two_days_ago, yesterday)
            )

            # Insert answers for questions
            for q_idx, q in enumerate(ds_questions):
                sel = q["ans"] if q_idx < cor else ("B" if q["ans"] != "B" else "A")
                is_cor = 1 if sel == q["ans"] else 0
                mk = q["marks"] if is_cor else 0.0
                cursor.execute(
                    """INSERT INTO student_answers (id, attempt_id, question_id, selected_option, is_correct, marks_obtained, is_marked_for_review, saved_at)
                       VALUES (?, ?, ?, ?, ?, ?, 0, ?);""",
                    (str(uuid.uuid4()), att_id, q["id"], sel, is_cor, mk, yesterday)
                )

            # Insert Result record
            res_id = str(uuid.uuid4())
            cursor.execute(
                """INSERT INTO results (id, attempt_id, exam_id, student_id, total_questions, correct_count, wrong_count,
                                       unanswered_count, total_marks, obtained_marks, percentage, grade, pass_fail, rank, generated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, 0, 8.0, ?, ?, ?, ?, ?, ?);""",
                (res_id, att_id, exam2_id, s["student_id"], len(ds_questions),
                 cor, len(ds_questions) - cor, score, pct, grd, res, rnk, yesterday)
            )

            # Insert Teacher Feedback
            fb_id = str(uuid.uuid4())
            cursor.execute(
                """INSERT INTO student_feedbacks (id, exam_id, student_id, teacher_id, attempt_id, feedback_text, rating, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);""",
                (fb_id, exam2_id, s["student_id"], teacher_records[1]["teacher_id"], att_id, fb_text, fb_rating, yesterday, yesterday)
            )

            # Insert Certificate if passed with honors
            if has_cert and ccode:
                cert_id = str(uuid.uuid4())
                cursor.execute(
                    """INSERT INTO certificates (id, certificate_code, attempt_id, exam_id, student_id, title, issue_date, expiry_date, verification_hash, status, created_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
                    (cert_id, ccode, att_id, exam2_id, s["student_id"],
                     "Data Structures Fundamentals Certification", yesterday, next_year,
                     hashlib.sha256(f"{ccode}:{s['student_id']}".encode()).hexdigest(),
                     "active", yesterday)
                )

        # Student performances across Exam 3 (DBMS & SQL Proficiency)
        db_perf_data = [
            # (student_index, correct_count, score, percentage, grade, pass_fail, rank, feedback_text, rating, has_cert, cert_code)
            (0, 4, 6.0, 100.0, "A+", "PASS", 1, "Flawless score on SQL queries, relational algebra, and ACID transaction semantics!", 5, True, "CERT-2026-DB-001"),
            (5, 4, 6.0, 100.0, "A+", "PASS", 1, "Exemplary understanding of SQL subqueries, join mechanics, and BCNF normalization.", 5, True, "CERT-2026-DB-002"),
            (2, 3, 5.0, 83.3, "A", "PASS", 3, "Strong command of transactional properties and indexing strategies. Excellent performance.", 4, False, None),
            (6, 3, 5.0, 83.3, "A", "PASS", 3, "Very good work on complex join operations. Continue strengthening query optimization.", 4, False, None),
            (1, 2, 4.0, 66.7, "B", "PASS", 5, "Good foundational understanding. Review group aggregations and having clauses.", 4, False, None),
            (3, 2, 4.0, 66.7, "B", "PASS", 5, "Solid baseline achieved. More practice with foreign key constraints recommended.", 3, False, None),
            (4, 1, 2.0, 33.3, "F", "FAIL", 7, "Struggled with SQL joins and normalization forms. Recommended for remedial tutoring session.", 2, False, None),
        ]

        for s_idx, cor, score, pct, grd, res, rnk, fb_text, fb_rating, has_cert, ccode in db_perf_data:
            if s_idx >= len(student_records):
                continue
            s = student_records[s_idx]
            att_id = str(uuid.uuid4())
            
            cursor.execute(
                """INSERT INTO exam_attempts (id, exam_id, student_id, start_time, end_time, time_remaining_seconds,
                                             status, total_score, percentage, grade, result, evaluated_at, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, 0, ?, ?, ?, ?, ?, ?, ?, ?);""",
                (att_id, exam3_id, s["student_id"], two_days_ago, yesterday, AttemptStatus.EVALUATED.value,
                 score, pct, grd, res, yesterday, two_days_ago, yesterday)
            )

            # Insert answers for questions
            for q_idx, q in enumerate(db_questions):
                sel = q["ans"] if q_idx < cor else ("B" if q["ans"] != "B" else "A")
                is_cor = 1 if sel == q["ans"] else 0
                mk = q["marks"] if is_cor else 0.0
                cursor.execute(
                    """INSERT INTO student_answers (id, attempt_id, question_id, selected_option, is_correct, marks_obtained, is_marked_for_review, saved_at)
                       VALUES (?, ?, ?, ?, ?, ?, 0, ?);""",
                    (str(uuid.uuid4()), att_id, q["id"], sel, is_cor, mk, yesterday)
                )

            # Insert Result record
            res_id = str(uuid.uuid4())
            cursor.execute(
                """INSERT INTO results (id, attempt_id, exam_id, student_id, total_questions, correct_count, wrong_count,
                                       unanswered_count, total_marks, obtained_marks, percentage, grade, pass_fail, rank, generated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, 0, 6.0, ?, ?, ?, ?, ?, ?);""",
                (res_id, att_id, exam3_id, s["student_id"], len(db_questions),
                 cor, len(db_questions) - cor, score, pct, grd, res, rnk, yesterday)
            )

            # Insert Teacher Feedback
            fb_id = str(uuid.uuid4())
            cursor.execute(
                """INSERT INTO student_feedbacks (id, exam_id, student_id, teacher_id, attempt_id, feedback_text, rating, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);""",
                (fb_id, exam3_id, s["student_id"], teacher_records[2]["teacher_id"], att_id, fb_text, fb_rating, yesterday, yesterday)
            )

            # Insert Certificate if passed with honors
            if has_cert and ccode:
                cert_id = str(uuid.uuid4())
                cursor.execute(
                    """INSERT INTO certificates (id, certificate_code, attempt_id, exam_id, student_id, title, issue_date, expiry_date, verification_hash, status, created_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
                    (cert_id, ccode, att_id, exam3_id, s["student_id"],
                     "DBMS & SQL Proficiency Certification", yesterday, next_year,
                     hashlib.sha256(f"{ccode}:{s['student_id']}".encode()).hexdigest(),
                     "active", yesterday)
                )

        # Student performances across Exam 1 (Python Programming)
        py_perf_data = [
            (0, 7, 13.0, 86.7, "A", "PASS", 2, "Great mastery of Python data structures, list comprehensions, and OOP patterns.", 5, True, "CERT-2026-PY-001"),
            (5, 8, 15.0, 100.0, "A+", "PASS", 1, "Perfect score across all advanced Python internals, decorators, and memory management.", 5, True, "CERT-2026-PY-002"),
            (2, 6, 11.0, 73.3, "B", "PASS", 3, "Solid command of syntax and standard libraries. Keep practicing context managers.", 4, False, None),
            (1, 5, 9.0, 60.0, "C", "PASS", 4, "Good progress on functions and dictionary methods.", 3, False, None),
            (4, 3, 5.0, 33.3, "F", "FAIL", 5, "Needs extra practice on regular expressions and list comprehensions.", 2, False, None),
        ]

        for s_idx, cor, score, pct, grd, res, rnk, fb_text, fb_rating, has_cert, ccode in py_perf_data:
            if s_idx >= len(student_records):
                continue
            s = student_records[s_idx]
            att_id = str(uuid.uuid4())
            
            cursor.execute(
                """INSERT INTO exam_attempts (id, exam_id, student_id, start_time, end_time, time_remaining_seconds,
                                             status, total_score, percentage, grade, result, evaluated_at, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, 0, ?, ?, ?, ?, ?, ?, ?, ?);""",
                (att_id, exam1_id, s["student_id"], two_days_ago, yesterday, AttemptStatus.EVALUATED.value,
                 score, pct, grd, res, yesterday, two_days_ago, yesterday)
            )

            for q_idx, q in enumerate(py_questions[:8]):
                sel = q["ans"] if q_idx < cor else ("B" if q["ans"] != "B" else "A")
                is_cor = 1 if sel == q["ans"] else 0
                mk = q["marks"] if is_cor else 0.0
                cursor.execute(
                    """INSERT INTO student_answers (id, attempt_id, question_id, selected_option, is_correct, marks_obtained, is_marked_for_review, saved_at)
                       VALUES (?, ?, ?, ?, ?, ?, 0, ?);""",
                    (str(uuid.uuid4()), att_id, q["id"], sel, is_cor, mk, yesterday)
                )

            res_id = str(uuid.uuid4())
            cursor.execute(
                """INSERT INTO results (id, attempt_id, exam_id, student_id, total_questions, correct_count, wrong_count,
                                       unanswered_count, total_marks, obtained_marks, percentage, grade, pass_fail, rank, generated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, 0, 15.0, ?, ?, ?, ?, ?, ?);""",
                (res_id, att_id, exam1_id, s["student_id"], 8,
                 cor, 8 - cor, score, pct, grd, res, rnk, yesterday)
            )

            fb_id = str(uuid.uuid4())
            cursor.execute(
                """INSERT INTO student_feedbacks (id, exam_id, student_id, teacher_id, attempt_id, feedback_text, rating, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);""",
                (fb_id, exam1_id, s["student_id"], teacher_records[0]["teacher_id"], att_id, fb_text, fb_rating, yesterday, yesterday)
            )

            if has_cert and ccode:
                cert_id = str(uuid.uuid4())
                cursor.execute(
                    """INSERT INTO certificates (id, certificate_code, attempt_id, exam_id, student_id, title, issue_date, expiry_date, verification_hash, status, created_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
                    (cert_id, ccode, att_id, exam1_id, s["student_id"],
                     "Python Programming Midterm Certification", yesterday, next_year,
                     hashlib.sha256(f"{ccode}:{s['student_id']}".encode()).hexdigest(),
                     "active", yesterday)
                )

        # 8. NOTIFICATIONS
        notifs = [
            (student_records[0]["user_id"], "Certificate Awarded!", "Congratulations! You have been awarded Certificate CERT-2026-DS-001 for Data Structures.", "certificate_awarded", yesterday),
            (student_records[0]["user_id"], "Teacher Feedback Received", "Prof. Robert Smith left feedback on your Data Structures quiz submission.", "feedback_received", yesterday),
            (student_records[1]["user_id"], "Result Published", "Your result for Data Structures Fundamentals Quiz is now available: Grade C (62.5%).", "result_available", yesterday),
            (principal_id, "Academic Executive Report", "ExamHub institutional assessment summary ready for review by the Principal.", "executive_report", now),
            (admin_id, "System Initialized", "ExamHub platform initialized with full synthetic curriculum fixtures.", "system_alert", now),
        ]
        for uid, title, msg, ntype, ts in notifs:
            cursor.execute(
                """INSERT INTO notifications (id, user_id, title, message, type, is_read, link, created_at)
                   VALUES (?, ?, ?, ?, ?, 0, NULL, ?);""",
                (str(uuid.uuid4()), uid, title, msg, ntype, ts)
            )

    logger.info("Database seeding completed successfully!")
    logger.info("Created Principal: principal_sharma / password123")
    logger.info(f"Created Admin: admin / password123")
    logger.info(f"Created {len(teacher_records)} Teachers (e.g. teacher_smith / password123)")
    logger.info(f"Created {len(student_records)} Students (e.g. student_alice / password123)")
    logger.info(f"Created {len(subject_records)} Subjects, {len(question_records)} Questions, Exams, Attempts, Feedback & Certificates.")

if __name__ == "__main__":
    from backend.app.database.schema import init_db
    init_db()
    seed_database(force_reseed=True)
