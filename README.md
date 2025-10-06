# Flask LMS
Flask LMS is a RESTful API that centralises student, teacher, and course data for educational institutions.

## Overview
This project demonstrates how a lightweight student‑information system (SIS) can be built using Flask blueprints, SQLAlchemy, and Marshmallow. It shows how schools moving off paper forms and spreadsheets could consolidate records behind a single source of truth and reduce duplicate data entry.

> **Disclaimer:** This project is provided as an educational exercise and is still in development. It is not production-ready and should not be used to manage real student data without further security and authentication features.

## Quick Setup
<details>
<summary><b>Instructions</b></summary>

All commands below are copy-paste ready. Replace placeholder values such as `your-username` or passwords as needed.

### 1. Clone the repository
```bash
git clone https://github.com/macfluffy/flask-lms.git
cd flask-lms
```
> Clone the repository and enter its directory.

### 2. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```
> macOS/Linux commands shown; see below for Windows virtual environment steps.
<!-- Windows virtual environment steps: -->

### 3. Install PostgreSQL
Make sure PostgreSQL (version 14 or higher) is installed and running on your system.

#### macOS (Homebrew)
```bash
brew install postgresql
brew services start postgresql
```
> macOS only; see Windows installation steps below.
<!-- Windows installation steps : -->

### 4. Create the database and user
```bash
psql -U postgres <<'SQL'
CREATE USER lms_user WITH PASSWORD 'change-me';
CREATE DATABASE lms_db OWNER lms_user;
SQL
```
> Replace 'change-me' with your own password. This one-liner runs the SQL inside psql automatically for easier setup.

### 5. Configure environment variables
Create a `.env` file in the project root to store your database connection details:
```bash
echo "DATABASE_URI=postgresql://lms_user:change-me@localhost:5432/lms_db" > .env
```
> The `.env` file contains sensitive info and is already in `.gitignore`. Be sure to use your actual password.

### 6. Create and seed the database
```bash
export FLASK_APP=main
flask db create
flask db seed
```
> On Windows Command Prompt use `set FLASK_APP=main`; in PowerShell use `$env:FLASK_APP = "main"`.

### 7. Start the development server
```bash
flask --app main run
```
> The API defaults to `http://127.0.0.1:5000/`.

</details>

## Background & rationale
Many schools still rely on paper forms or disconnected spreadsheets, which leads to delays, duplicated effort, and high administrative workload. Moving to a centralised student‑information system reduces manual entry and makes daily tasks more efficient.

Research highlights the value of this shift:
- Paperless administration helps schools improve compliance and productivity. [(School Governance, 2019)](https://www.schoolgovernance.net.au/news/schools-can-bloom-in-a-paperless-future)
- Australian teachers spend more time on administration than the OECD average, reinforcing the need for streamlined systems. [(AEU/TALIS report)](https://www.aeuvic.asn.au/australian-teachers-have-higher-workloads-fewer-resources-oecd-report)
- International guidance (EMIS) stresses the importance of centralising student information for effective data management. [(OECD Digital Education Outlook, 2023)](https://www.oecd.org/en/publications/oecd-digital-education-outlook-2023_c74f03de-en/full-report/education-and-student-information-systems_ef9f7b25.html)

## Target users & sample user stories
- **School administrator:** As an administrator, I want to avoid double‑entering data from paper forms so that enrolment is quicker and records stay consistent.
- **Teacher:** As a teacher, I want less administrative paperwork and quick access to my courses so that I can focus more on teaching and assessment.
- **Policy/IT perspective:** As a policy maker, I want centralised student information so that schools can manage and share data more effectively.

## Features
- RESTful CRUD endpoints for students, teachers, and courses with JSON responses.
- Blueprint-based routing with Marshmallow schemas for clean serialization.
- PostgreSQL persistence via SQLAlchemy models and relationships.
- CLI helpers (`flask db create|drop|seed`) for rapid database lifecycle management.
- Environment-based configuration using `.env` and `python-dotenv`.
- Basic error handling for integrity violations and missing resources.


## API Reference
Base URL: `http://localhost:5000`
Endpoints include:
- `/students`
- `/teachers`
- `/courses`

## Security & data considerations
- **Authentication & authorisation:** Not implemented yet. A production deployment must add secure login and role-based access (e.g., admin, teacher, read-only) to protect records.
- **Data protection (PII):** The system handles names, emails, and addresses. In production, traffic must use TLS (HTTPS) and at-rest protection (e.g., encrypted volumes, restricted DB access).
- **Error handling:** Some endpoints currently return raw database error details. Replace with sanitised error responses and structured error codes in production.
- **Secrets & configuration:** Database credentials live in `.env` (excluded from Git). Use strong, rotated passwords or managed secrets; never commit secrets to source control.

## Similar projects & inspiration
Large-scale systems such as [Moodle](https://moodle.org/), [Blackboard](https://www.anthology.com/blackboard), and [Canvas](https://www.instructure.com/canvas) are widely used by schools and universities to manage courses, enrolments, and student data.

Flask LMS is inspired by these platforms but intentionally scoped as a lightweight educational demonstration. It provides a smaller-scale example of how course, teacher, and student records can be centralised in a single system for learning and development purposes.

## References
- School Governance (2019). *Schools can bloom in a paperless future.* https://www.schoolgovernance.net.au/news/schools-can-bloom-in-a-paperless-future
- AEU Victoria (n.d.). *Australian teachers have higher workloads, fewer resources: OECD report (TALIS).* https://www.aeuvic.asn.au/australian-teachers-have-higher-workloads-fewer-resources-oecd-report
- OECD (2023). *Digital Education Outlook 2023 — Education and Student Information Systems (EMIS).* https://www.oecd.org/en/publications/oecd-digital-education-outlook-2023_c74f03de-en/full-report/education-and-student-information-systems_ef9f7b25.html
