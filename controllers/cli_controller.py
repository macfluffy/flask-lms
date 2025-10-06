from flask import Blueprint
from init import db

from models.student import Student
from models.teacher import Teacher
from models.course import Course
from models.enrolment import Enrolment

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created.")

@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped.")

@db_commands.cli.command("seed")
def seed_tables():
    # Create an instance of the model
    students = [Student(
        first_name = "Alice",
        last_name = "Son",
        email = "alice@email.com",
        phone = "12345678",
        address = "Sydney"
    ), Student(
        first_name = "Bob",
        last_name = "Aliceson",
        email = "bob@email.com",
        phone = "67891234",
        address = "Brisbane"
    )]

    # Add to the session
    db.session.add_all(students)

    teachers = [Teacher(
        first_name = "Teacher",
        last_name = "1",
        department = "Science",
        address = "Sydney",
        phone = "0412345678",
        email = "teacher1@email.com"
    ), Teacher(
        first_name = "Teacher",
        last_name = "2",
        department = "Management",
        address = "Brisbane",
        phone = "98091234",
        email = "teacher2@email.com"
    )]

    db.session.add_all(teachers)
    # Commit to the session
    db.session.commit()

    courses = [Course(
        name = "Physics",
        duration = 3,
        teacher_id = teachers[0].teacher_id
    ), Course(
        name = "Chemistry",
        duration = 3,
        teacher_id = teachers[0].teacher_id
    ), Course(
        name = "Biology",
        duration = 3,
        teacher_id = teachers[0].teacher_id
    ), Course(
        name = "Mathematics",
        duration = 3,
        teacher_id = teachers[1].teacher_id
    ), Course(
        name = "Accounting",
        duration = 3,
        teacher_id = teachers[1].teacher_id
    )]

    db.session.add_all(courses)
    db.session.commit()

    enrolments = [
        Enrolment(
            enrolment_date = "2025-09-29",
            student_id = students[0].student_id,
            course_id = courses[0].course_id
        ),
        Enrolment(
            enrolment_date = "2025-09-29",
            student_id = students[1].student_id,
            course_id = courses[1].course_id
        ),
        Enrolment(
            enrolment_date = "2025-09-29",
            student_id = students[0].student_id,
            course_id = courses[1].course_id
        )
    ]

    db.session.add_all(enrolments)
    db.session.commit()
    print("Tables created.")