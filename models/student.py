"""
This file defines the model for the 'students' table and it's relationships. 
"""

# Local imports
from init import db

class Student(db.Model):
    """
    The student table template. This contains the columns for their name, 
    their contact details, and their enrolments to courses.
    """

    # Name of the table and what is referenced by Flask-SQLAlchemy methods
    __tablename__ = "students"

    # Table columns
    student_id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(100), nullable = False)
    last_name = db.Column(db.String(100), nullable = False)

    # Table columns (Contact Details) - For privacy concerns these can be left empty
    # Only exception is email, as this is the student's email and there needs to be 
    # some way to contact the student
    email = db.Column(db.String(100), nullable = False, unique = True)
    address = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    """
    Define the relationship between students and the courses they are enroled in.
    An enrolment can't exist if there is no student to attend the course
    """
    # Delete enrolments associated to the student when they are deleted
    enrolments = db.relationship(
        "Enrolment", 
        back_populates = "student", 
        cascade = "all, delete"
    )