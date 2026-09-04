# ExamHub — Enterprise Examination Management System

ExamHub is a full-stack, secure, production-grade examination management platform designed for educational institutions, academies, and certification authorities. It features automated and manual exam creation, real-time proctored candidate test sessions, psychometric analytics, customizable grading rubrics, verifiable digital certificates, and comprehensive role-based access control.

---

## Key Features

- **Candidate Examination Portal**: Timed online assessments with autosaving, question navigation palette, review marking, and instant result scorecards.
- **Continuous Live Proctoring**: Real-time detection and audit logging of tab switching, window blur, multi-display anomalies, and candidate integrity metrics.
- **Automated & Manual Question Studio**: Rich question builder supporting multiple-choice questions, difficulty ratings, topic tagging, LaTeX math equations, and explanations.
- **Psychometric Analytics Engine**: Advanced psychometric measurement including Item Difficulty Index ($P$), Item Discrimination Index ($D$), Point-Biserial Correlations ($r_{pbis}$), score distributions, and cohort comparisons.
- **Verifiable Digital Certificates**: Cryptographically signed certificates of completion with unique serial IDs, verification QR data, and print-ready templates.
- **Role-Based Access Control (RBAC)**: Distinct permissions and personalized dashboards for Administrators, Teachers/Instructors, and Students.
- **Export & Import Suite**: Full export support for CSV score sheets, JSON exam archives, and Aiken/GIFT format question bank ingestion.
- **Dark Mode Support**: High-contrast, themeable user interface tailored for long testing sessions.

---

## Architecture Overview

- **Frontend**: React 19, TypeScript, Tailwind CSS, Vite, Lucide Icons.
- **Backend API**: Python 3.12+, FastAPI, SQLite3 with WAL mode, Uvicorn ASGI server.
- **Authentication**: JWT (JSON Web Tokens) with PBKDF2-SHA256 password hashing.
- **Database Engine**: Relational schema with foreign-key integrity, transactional rollbacks, and automated seeding.

---

## Installation

### Prerequisites
- Node.js (v18.0.0 or higher)
- Python (v3.10 or higher)
- pip and npm package managers

### 1. Clone the Repository
```bash
git clone https://github.com/examhub/examhub.git
cd examhub
```

### 2. Install Frontend Dependencies
```bash
npm install
```

### 3. Install Backend Dependencies
```bash
pip install -r requirements.txt
```

---

## Build

To compile and produce the production-ready frontend bundle:

```bash
npm run build
```

This compiles TypeScript source files, bundles assets via Vite into the `dist/` directory, and ensures type integrity without errors.

---

## Running the Application

### Development Mode

1. **Start the Backend API Server (Port 8001)**:
```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8001 --reload
```
Alternatively:
```bash
python backend/app/main.py
```

2. **Start the Frontend Development Server (Port 3000)**:
```bash
npm run dev
```

3. **Access the Web Application**:
Open your web browser and navigate to `http://localhost:3000`.

### Production Deployment

1. Build the frontend bundle:
```bash
npm run build
```

2. Run the production ASGI server:
```bash
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8001 --workers 4
```

---

## Testing & Quality Assurance

### Run Backend Test Suite
```bash
python -m pytest backend/tests -v
```

### Run Production Measurement & Audit
```bash
python measure.py
```

### Run TypeScript Type Check
```bash
npm run lint
```

---

## Default Demo Credentials

For quick evaluation and local demonstration, the system comes seeded with the following synthetic persona accounts:

| Role | Username | Password | Notes |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `password123` | Full administrative control, user & subject management |
| **Teacher** | `teacher_smith` | `password123` | Exam authoring, question studio, results inspection |
| **Student** | `student_alice` | `password123` | Timed examination candidate (Roll STU001) |
| **Student** | `student_carol` | `password123` | Alternate candidate (Roll STU002) |

---

## License & Ownership

Proprietary Software. Copyright &copy; 2026 ExamHub Technologies. All rights reserved. Unauthorized copying, distribution, or decompilation of this software via any medium is strictly prohibited.
