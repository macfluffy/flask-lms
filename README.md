# Flask LMS
Flask LMS is a RESTful API designed for accessing and maintaining course, student, and teacher data for educational institutions.
The API is structured to present information in a way that is most relevant to teachers and administrators.

## Overview
Flask LMS is a RESTful service that provides a clean CRUD backend for managing students, teachers, and courses in an educational setting. It uses Flask blueprints, SQLAlchemy models, and Marshmallow schemas to deliver a modular, maintainable API surface. The system follows industry conventions for clarity, ease of setup, and extensibility.

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

# macOS (Homebrew)
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
