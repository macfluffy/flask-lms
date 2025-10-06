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
    """
    The student schema template. This organises the JSON response when fetching student
    information such as their name, their contact details, and their enrolments to 
    courses.
    """
    class Meta:
        model = Student
        load_instance = True

        # Define the exact order of how the JSON query is displayed
        # Name, Enrolments, Contact Details
        fields = (
            "student_id", 
            "first_name", 
            "last_name", 
            "enrolments", 
            "email", 
            "phone", 
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

# Create instances of the schema for the controllers to call when applying validation,
# error handling and restrictions
student_schema = StudentSchema()
students_schema = StudentSchema(many = True)


class TeacherSchema(SQLAlchemyAutoSchema):
    """
    The teacher schema template. This organises the JSON response when fetching teacher
    information such as their name, their contact details, the department they work in,
    and the courses they teach.
    """
    class Meta:
        model = Teacher
        load_instance = True
        
        # Define the exact order of how the JSON query is displayed
        # Name, Department, Courses, Contact Details
        fields = (
            "teacher_id", 
            "first_name", 
            "last_name", 
            "department", 
            "courses", 
            "address",
            "phone",
            "email"
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

# Create instances of the schema for the controllers to call when applying validation,
# error handling and restrictions
teacher_schema = TeacherSchema()
teachers_schema = TeacherSchema(many = True)


class CourseSchema(SQLAlchemyAutoSchema):
    """
    The course schema template. This organises the JSON response when fetching course
    information such as the name of the course, how long the course will run for,
    who will be teaching the course, and those who are enrolled in this course.
    """
    class Meta:
        model = Course
        load_instance = True
        include_fk = True
        
        # Define the exact order of how the JSON query is displayed
        # Name, Duration, Course Teacher, Student Enrolments
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
    @validates('duration')
    def validates_duration(self, duration, data_key):
        if duration <= 1:
            raise ValidationError("Duration can't be less than 1.")

    # Only show the teacher's name and the department they work in
    # when showing the teacher teaching this course
    teacher = fields.Nested(
        "TeacherSchema", 
        dump_only = True, 
        only = (
            "first_name", 
            "last_name", 
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

# Create instances of the schema for the controllers to call when applying validation,
# error handling and restrictions
course_schema = CourseSchema()
courses_schema = CourseSchema(many = True)


class EnrolmentSchema(SQLAlchemyAutoSchema):
    """
    The enrolment schema template. This organises the JSON response when fetching 
    enrolment information such as when this enrolment was created, the enrolling 
    student and the course they've enrolled in.
    """
    class Meta:
        model = Enrolment
        load_instance = True
        include_fk = True

        # Define the exact order of how the JSON query is displayed
        # Enrolment Date, Enrolling Student, Course Being Taken
        fields = (
            "id", 
            "enrolment_date", 
            "student", 
            "course"
        )

    # Only show the student's name when showing student information in
    # the enrolment query
    student = fields.Nested(
        "StudentSchema", 
        only = (
            "student_id", 
            "first_name",
            "last_name",
        )
    )

    # Only show the name of the course and how long it takes to complete
    # in the enrolment query
    course = fields.Nested(
        "CourseSchema", 
        only = (
            "course_id", 
            "name", 
            "duration"
        )
    )

# Create instances of the schema for the controllers to call when applying validation,
# error handling and restrictions
enrolment_schema = EnrolmentSchema()
enrolments_schema = EnrolmentSchema(many = True)