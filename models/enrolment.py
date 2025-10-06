"""
This file defines the model for the 'enrolments' junction table and it's relationships with
'students' and the 'courses' models. 
"""

# Built-in imports
from datetime import date

# Local imports
from init import db

class Enrolment(db.Model):
    """
    The enrolment table template contains the information about a student's
    enrolment in a course. Enrolments cannot exist without either a student
    or a course.
    """

    # Name of the table and what is referenced by Flask-SQLAlchemy methods
    __tablename__ = "enrolments"
    
    # Create a unique constraint that prevents duplicate enrolment entries of
    # with the same student and course combination
    __table_args__ = (
        db.UniqueConstraint(
            "student_id", 
            "course_id", 
            name = "enrolments_unique_student_course"
        ),
    )

    # Table columns
    id = db.Column(db.Integer, primary_key = True)
    enrolment_date = db.Column(db.Date, default = date.today)
    student_id = db.Column(db.Integer, db.ForeignKey("students.student_id"), nullable = False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.course_id"), nullable = False)

    # Define the relationships between courses, students, and enrolments
    student = db.relationship("Student", back_populates = "enrolments")
    course = db.relationship("Course", back_populates = "enrolments")