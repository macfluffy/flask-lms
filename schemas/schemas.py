"""
This file creates the structure on how the data should be organised within our relational database,
their constraints, and the relationships between each of these tables.
"""

# Installed import packages
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow.validate import Length, Regexp, Range, OneOf
from marshmallow import fields, ValidationError, validates

# Local imports - Tables
from models.student import Student
from models.teacher import Teacher
from models.course import Course
from models.enrolment import Enrolment


class StudentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        load_instance = True

        # Define the exact order of how the JSON query is displayed
        fields = (
            "student_id", 
            "name", 
            "email", 
            "enrolments", 
            "address"
        )
    
    # Exclude argument takes a tuple, thus the comma with no additional arguments at the end is to denote a tuple
    # Student is excluded to prevent reference recursion when displaying a student's enrolment information
    enrolments = fields.List(
        fields.Nested(
            "EnrolmentSchema", 
            exclude = ("student",)
        )
    )

student_schema = StudentSchema()
students_schema = StudentSchema(many = True)


class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        load_instance = True
        
        # Define the exact order of how the JSON query is displayed
        fields = (
            "teacher_id", 
            "name", 
            "department", 
            "courses", 
            "address"
        )

    # The valid department values: Science, Management, Engineering
    department = auto_field(
        validate = OneOf(
            [
                "Science", 
                "Management", 
                "Engineering"
            ], 
            error = "Only valid departments are: Science, Management, and Engineering."
        )
    )
    # Exclude teachers to prevent reference recursion when displaying the course information
    courses = fields.List(
        fields.Nested(
            "CourseSchema", 
            exclude = (
                "teacher", 
                "teacher_id"
            )
        )
    )

teacher_schema = TeacherSchema()
teachers_schema = TeacherSchema(many = True)


class CourseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Course
        load_instance = True
        include_fk = True
        
        # Define the exact order of how the JSON query is displayed
        fields = (
            "course_id", 
            "name", 
            "duration", 
            "teacher_id", 
            "teacher", 
            "enrolments"
        )

    # name: cannot be blank, starts with letter, allows letters/numbers/spaces
    name = auto_field(
        validate = [
            Length(
                min = 3, 
                max = 50, 
                error = "Course cannot be less than 3  or more than 50 characters in length."
            ), 
            Regexp(
                r"^[A-Za-z][A-Za-z0-9 ]*$",
                error = "Name must start with a letter and must contain only letters, numbers and spaces."
            )
        ]
    )

    # Course duration has to be greater than 0
    # Method 1: Use "validate" argument
    # duration = auto_field(
    #     validate = [
    #         Range(
    #             min = 1,
    #             min_inclusive = 1,
    #             error = "Duration must be greater or equal than 1."
    #         )
    #     ]
    # )
    # Method 2: Use @validate decorator
    # @validates('property-to-validate')
    # def fn_name(se;f, property-to-validate, data_key)
    @validates('duration')
    def validates_duration(self, duration, data_key):
        if duration <= 1:
            raise ValidationError("Duratiocan't be less than 1.")

    teacher = fields.Nested(
        "TeacherSchema", 
        dump_only = True, 
        only = (
            "name", 
            "department"
        )
    )

    # Exclude argument takes a tuple, thus the comma with no additional arguments at the end is to denote a tuple
    # Exclude course to prevent reference recursion when displaying the enrolment information
    enrolments = fields.List(
        fields.Nested(
            "EnrolmentSchema", 
            exclude = ("course",)
        )
    )

course_schema = CourseSchema()
courses_schema = CourseSchema(many = True)


class EnrolmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Enrolment
        load_instance = True
        include_fk = True

        # Define the exact order of how the JSON query is displayed
        fields = (
            "id", 
            "enrolment_date", 
            "student", 
            "course"
        )

    student = fields.Nested(
        "StudentSchema", 
        only = (
            "student_id", 
            "name"
        )
    )

    course = fields.Nested(
        "CourseSchema", 
        only = (
            "course_id", 
            "name", 
            "duration"
        )
    )

enrolment_schema = EnrolmentSchema()
enrolments_schema = EnrolmentSchema(many = True)