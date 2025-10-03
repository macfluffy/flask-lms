"""
The enrolment table template contains the information about a student's
enrolment in a course. Enrolments cannot exist without a student or a
course.
"""

# Built-in imports
from datetime import date

# Local imports
from init import db

class Enrolment(db.Model):
    __tablename__ = "enrolments"
    __table_args__ = (
        db.UniqueConstraint("student_id", "course_id", name = "enrolments_unique_student_course"),
    )

    # Table columns
    id = db.Column(db.Integer, primary_key = True)
    enrolment_date = db.Column(db.Date, default = date.today)
    student_id = db.Column(db.Integer, db.ForeignKey("students.student_id"), nullable = False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.course_id"), nullable = False)

    # Define the relationships between courses, students, and enrolments
    student = db.relationship("Student", back_populates = "enrolments")
    course = db.relationship("Course", back_populates = "enrolments")