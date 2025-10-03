"""
The student table template. This contains the columns for their name, 
their contact details, and their enrolments to courses.
"""

# Local imports
from init import db

class Student(db.Model):
    __tablename__ = "students"

    # Table columns
    student_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    address = db.Column(db.String(100)) 

    # Define the relationship between students and their enrolments
    enrolments = db.relationship("Enrolment", back_populates = "student", cascade = "all, delete")