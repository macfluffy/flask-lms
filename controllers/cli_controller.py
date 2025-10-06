"""
This file creates the Create, Read, Update, and Delete operations to our command
line interface through REST API design using Flask Blueprint. This file creates
the commands to automate the creation and seeding of the LMS database.
"""

# Installed import packages
from flask import Blueprint

# Local imports
from init import db
from models.student import Student
from models.teacher import Teacher
from models.course import Course
from models.enrolment import Enrolment

# Create the Template Application Interface for in-line command routes to be applied 
# to the Flask application
db_commands = Blueprint("db", __name__)


"""
API Routes
"""

@db_commands.cli.command("create")
def create_tables():
    """
    Creates all the tables as defined in the models subfolder
    """
    db.create_all()
    print("Tables created.")

@db_commands.cli.command("drop")
def drop_tables():
    """
    This function deletes all tables and leaves an empty database
    """
    db.drop_all()
    print("Tables dropped.")

@db_commands.cli.command("seed")
def seed_tables():
    """
    Populate the table with initial data. Student, teacher, course,
    and enrolment information is added into the LMS database.
    """
    # Create students to add to the students database
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

    # Add the student information to this session
    db.session.add_all(students)

    # Create teachers to add to the teachers database
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

    # Add the teacher information to this session
    db.session.add_all(teachers)
    
    # Commit to the session and permanently add the teachers and students
    # to the database.
    db.session.commit()

    # Create courses to add to the courses database. Each course needs 
    # an assigned teacher so this must be created after teachers have 
    # been created.
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

    # Add the course information to this session
    db.session.add_all(courses)

    # Commit to the session and permanently add the courses to the 
    # database.
    db.session.commit()

    # Create enrolments to add to the enrolments database. Each 
    # enrolment needs a student and a course before this can be 
    # created.
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

    # Add the enrolment information to this session
    db.session.add_all(enrolments)

    # Commit to the session and permanently add the enrolments to the 
    # database.
    db.session.commit()
    print("Tables created.")