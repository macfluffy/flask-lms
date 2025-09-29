from init import db

class Course(db.Model):
    __tablename__ = "courses"

    course_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False, unique = True)
    duration = db.Column(db.Float, nullable = False)
    
    # Foreign Key
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.teacher_id"), nullable = False)
    # back_populates
    teacher = db.relationship("Teacher", back_populates = "courses")
    # back_refs

    enrolments = db.relationship("Enrolment", back_populates = "course")