from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

from models.student import Student
from models.teacher import Teacher
from models.course import Course

class StudentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        load_instance = True

student_schema = StudentSchema()
students_schema = StudentSchema(many = True)

class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        load_instance = True
        # Define the exact order of keys
        fields = ("teacher_id", "name", "department", "courses", "address")

    # Exclude teachers to prevent recursion, the comma at the end is to denote a tuple
    courses = fields.List(fields.Nested("CourseSchema", exclude = ("teacher", "teacher_id")))

teacher_schema = TeacherSchema()
teachers_schema = TeacherSchema(many = True)

class CourseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Course
        load_instance = True
        include_fk = True
        # Define the exact order of keys
        fields = ("course_id", "name", "duration", "teacher", "teacher_id")

    teacher = fields.Nested("TeacherSchema", dump_only = True, only = ("teacher_id", "name", "department"))

course_schema = CourseSchema()
courses_schema = CourseSchema(many = True)