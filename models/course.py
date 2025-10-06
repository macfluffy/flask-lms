"""
This file defines the model for the 'course' table and it's relationships with
'teachers' and the 'enrolments' models. 
"""

# Local imports
from init import db

class Course(db.Model):
    """
    The course table template contains the names of the course, the duration
    the course will run til completion, and the teacher who will be teaching
    it. 
    """

    # Name of the table and what is referenced by Flask-SQLAlchemy methods
    __tablename__ = "courses"

    # Table columns
    course_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False, unique = True)
    duration = db.Column(db.Float, nullable = False)
    
    # Foreign Key: Teacher ID is the common link between 
    # the course and teacher tables
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.teacher_id"))
    
    # Define the relationship between teachers teaching courses, and 
    # student course enrolments
    teacher = db.relationship("Teacher", back_populates = "courses")
    enrolments = db.relationship("Enrolment", back_populates = "course")