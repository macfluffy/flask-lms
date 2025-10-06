"""
This file defines the model for the 'teachers' table and it's relationships. 
"""

# Local imports
from init import db

class Teacher(db.Model):
    """
    This is the template for the teacher table. This table contains the name 
    and contact details of the teacher, the department they work in, and 
    what courses they are teaching.
    """

    # Name of the table and what is referenced by Flask-SQLAlchemy methods
    __tablename__ = "teachers"

    # Table columns
    teacher_id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(100), nullable = False)
    last_name = db.Column(db.String(100), nullable = False)
    department = db.Column(db.String(100), nullable = False)
    
    # Table columns (Contact Details) - For privacy concerns these can be left empty
    address = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    email = db.Column(db.String(100))   

    # Define the relationship between teachers and the courses they are teaching
    # When a teacher leaves, the course can still continue to exist
    courses = db.relationship(
        "Course", 
        back_populates = "teacher", 
        cascade = "all, set null"
    )