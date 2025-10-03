"""
The teacher table template. This table contains the name and
contact details of the teacher, the department they work in,
and what courses they are teaching.
"""

# Local imports
from init import db

class Teacher(db.Model):
    __tablename__ = "teachers"

    # Table columns
    teacher_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    department = db.Column(db.String(100), nullable = False)
    address = db.Column(db.String(100))

    # Define the relationship between teachers and the courses they are teaching
    courses = db.relationship("Course", back_populates = "teacher", cascade = "all, delete-orphan")