from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow.validate import Length, Regexp, Range
from marshmallow import fields

from models.student import Student
from models.teacher import Teacher
from models.course import Course
from models.enrolment import Enrolment

class StudentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        load_instance = True
        fields = ("student_id", "name", "email", "enrolments", "address")

    enrolments = fields.List(fields.Nested("EnrolmentSchema", exclude = ("student",)))

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
        fields = ("course_id", "name", "duration", "teacher", "enrolments")

    # name: cannot be blank, starts with letter, allows letters/numbers/spaces
    name = auto_field(validate = [
        Length(
            min = 3, 
            max = 50, 
            error = "Course cannot be less than 3  or more than 50 characters in length."
        ), 
        Regexp(
            r"^[A-Za-z][A-Za-z0-9 ]*$",
            error = "Name must start with a letter and must contain only letters, numbers and spaces."
        )
    ])

    duration = auto_field(validate = [
        Range(
            min = 1,
            min_inclusive = 1,
            error = "Duration must be greater or equal than 1."
        )
    ])

    teacher = fields.Nested("TeacherSchema", dump_only = True, only = ("name", "department"))
    enrolments = fields.List(fields.Nested("EnrolmentSchema", exclude = ("course",)))

course_schema = CourseSchema()
courses_schema = CourseSchema(many = True)

class EnrolmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Enrolment
        load_instance = True
        include_fk = True
        fields = ("id", "enrolment_date", "student", "course")

    student = fields.Nested("StudentSchema", only = ("student_id", "name"))
    course = fields.Nested("CourseSchema", only = ("course_id", "name", "duration"))

enrolment_schema = EnrolmentSchema()
enrolments_schema = EnrolmentSchema(many = True)