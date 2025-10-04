# Flask LMS
Flask LMS is a RESTful API designed for accessing and maintaining course, student, and teacher data for educational institutions.
The API is structured to present information in a way that is most relevant to teachers and administrators.

## Overview
Flask LMS models a simple student‑information system (SIS): it centralises students, teachers and courses in one PostgreSQL‑backed service and exposes them via a small REST API. It is suitable for demonstrating how a school moving off paper forms and spreadsheets could consolidate records behind a single source of truth and reduce duplicate data entry.

## Problem & context
Many schools are modernising administration processes that still rely on paper and disconnected spreadsheets. International guidance highlights the role of student‑information systems (also known as EMIS) in helping institutions consolidate data and streamline operations. In Australia, teacher workload and time spent on administration are consistently high, which strengthens the case for lightweight, purpose‑built data systems schools can run and extend.

- **Why centralise?** Education management information systems help countries and schools manage data effectively and support decision‑making. See the OECD Digital Education Outlook for a synthesis of how SIS/EMIS fit within national digital education ecosystems. [(OECD, 2023)](https://www.oecd.org/en/publications/oecd-digital-education-outlook-2023_c74f03de-en/full-report/education-and-student-information-systems_ef9f7b25.html)
- **Workload pressure:** Australian teachers report higher administrative load than the OECD average, with administration time rising relative to peers. AEU’s summary of TALIS findings highlights administration as a key workload issue. [(AEU, citing OECD TALIS)](https://www.aeuvic.asn.au/australian-teachers-have-higher-workloads-fewer-resources-oecd-report)
- **Moving beyond paper:** Sector commentary argues that paper‑based admin slows compliance and productivity, and that schools benefit from digital processes. [(School Governance, 2019)](https://www.schoolgovernance.net.au/news/schools-can-bloom-in-a-paperless-future)

## Target users & sample user stories
- **School administrator:** “Register a new student and enrol them into a course so that records are consistent and searchable across departments.”
- **Teacher:** “View my courses and class lists so I can update attendance and assessments without relying on paper forms.”

## Quick Setup
All commands below are copy-paste ready. Replace placeholder values such as `your-username` or passwords as needed.

### 1. Clone the repository
```bash
git clone https://github.com/macfluffy/flask-lms.git
cd flask-lms
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```
<!-- Windows virtual environment steps: -->

### 3. Install PostgreSQL
Make sure PostgreSQL (version 14 or higher) is installed and running on your system.

### macOS (Homebrew)
```bash
brew install postgresql
brew services start postgresql
```
<!-- Windows installation steps : -->

### 4. Create the database and user
```bash
psql -U postgres <<'SQL'
CREATE DATABASE lms_db;
CREATE USER lms_user WITH PASSWORD 'change-me';
GRANT ALL PRIVILEGES ON DATABASE lms_db TO lms_user;
SQL
```

### 5. Configure environment variables
Create a `.env` file in the project root to store your database connection details:
```bash
echo "DATABASE_URI=postgresql://lms_user:change-me@localhost:5432/lms_db" > .env
```
> The `.env` file contains sensitive information. It is already listed in `.gitignore` so it won’t be pushed to Git. Be sure to replace `change-me` with your own secure password.

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
The API defaults to `http://127.0.0.1:5000/`.

## Features
- RESTful CRUD endpoints for students, teachers, and courses with JSON responses.
- Blueprint-based routing with Marshmallow schemas for clean serialization.
- PostgreSQL persistence via SQLAlchemy models and relationships.
- CLI helpers (`flask db create|drop|seed`) for rapid database lifecycle management.
- Environment-based configuration using `.env` and `python-dotenv`.
- Basic error handling for integrity violations and missing resources.

## References
- OECD (2023). *Digital Education Outlook 2023 — Education and Student Information Systems (EMIS).* https://www.oecd.org/en/publications/oecd-digital-education-outlook-2023_c74f03de-en/full-report/education-and-student-information-systems_ef9f7b25.html
- AEU Victoria (n.d.). *Australian teachers have higher workloads, fewer resources: OECD report (TALIS).* https://www.aeuvic.asn.au/australian-teachers-have-higher-workloads-fewer-resources-oecd-report
- School Governance (2019). *Schools can bloom in a paperless future.* https://www.schoolgovernance.net.au/news/schools-can-bloom-in-a-paperless-future

## API Reference
Base URL: `http://localhost:5000`
Endpoints include:
- `/students`
- `/teachers`
- `/courses`


## Steps to run the API
- Create a database, user with Read/Write privileges to the database
- Create an .env file
- Define the DATABASE_URI value
