"""
This file creates the Create, Read, Update, and Delete operations to our student data,
through REST API design using Flask Blueprint.
"""

# Installed import packages
from flask import Blueprint, jsonify, request

# Local imports
from init import db
from models.student import Student
from schemas.schemas import student_schema, students_schema


# Create the Template Web Application Interface for student routes to be applied 
# to the Flask application
students_bp = Blueprint("students", __name__, url_prefix = "/students")


"""
Student Controller Error Messages
"""

def error_empty_table():
    return {"message": "No records found. Add a statement to get started."}

def error_student_does_not_exist(student_id):
    return {"message": f"Student with id {student_id} does not exist"}, 404

def student_successfully_removed(first_name, last_name):
    return {"message": f"Student {first_name} {last_name} deleted successfully."}, 200 


"""
API Routes
"""

@students_bp.route("/")
def get_students():
    """
    Retrieve and read all the students from the student database,
    this is the equivalent of GET in postgresql.
    """
    # Selects all the students from the database
    statement = db.select(Student)
    students_list = db.session.scalars(statement)

    # Serialise it as the scalar result is unserialised
    queryData = students_schema.dump(students_list)
    
    # Return the search results if there are students in the student database, 
    # otherwise inform the user that the database is empty.
    if queryData:
        # Return the list of students in JSON format
        return jsonify(queryData)
    else:
        # Return an error message: Student table is empty
        return error_empty_table()


@students_bp.route("/<int:student_id>")
def get_a_student(student_id):
    """
    Retrieve and read a specific student's information from 
    the student database, using the student ID as the marker.
    """
    # Selects all the students from the database and filter the student with
    # matching ID
    statement = db.select(Student).where(Student.student_id == student_id)
    student = db.session.scalar(statement)

    # Serialise it as the scalar result is unserialised
    queryData = student_schema.dump(student)

    # Return the search results if this student is in the student database, 
    # otherwise inform the user that the student does not exist.
    if queryData:
        # Return the student info in JSON format
        return jsonify(queryData)
    else:
        # Return an error message: Student with this ID does not exist
        return error_student_does_not_exist(student_id)


@students_bp.route("/", methods = ["POST"])
def create_student():
    """
    Retrieve the body data and add the details of the student into the student database,
    this is the equivalent of POST in postgresql.
    """
    # Fetch the student information from the request body
    bodyData = request.get_json()
    
    # Create a new student object with the request body data as the attributes
    newStudent = Student(
        first_name = bodyData.get("first_name"),
        last_name = bodyData.get("last_name"),
        email = bodyData.get("email"),
        phone = bodyData.get("phone"),
        address = bodyData.get("address")
    )

    # Add the student data into the session
    db.session.add(newStudent)
    
    # Commit and write the student data from this session into 
    # the postgresql database
    db.session.commit()

    # Send acknowledgement
    acknowledgement = student_schema.dump(newStudent)
    return jsonify(acknowledgement), 201


@students_bp.route("/<int:student_id>", methods = ["DELETE"])
def delete_student(student_id):
    """
    Find the student with the matching ID in the student database and remove them.
    This is the equivalent of DELETE in postgresql.
    """
    # Selects all the students from the database and filter the student with
    # matching ID
    statement = db.select(Student).where(Student.student_id == student_id)
    student = db.session.scalar(statement)

    # Delete the student from the students database if they exist
    if student:
        # Remove the student from the session
        db.session.delete(student)
        
        # Commit and permanently remove the student data from the 
        # postgresql database
        db.session.commit()
        
        # Return an acknowledgement
        return student_successfully_removed(student.first_name, student.last_name)
    else:
        # Return an error message: Student with this ID does not exist
        return error_student_does_not_exist(student_id)

@students_bp.route("/<int:student_id>", methods = ["PUT", "PATCH"])
def update_student(student_id):
    """
    Retrieve the body data and update the details of the student with the 
    matching ID in the student database, this is the equivalent of 
    PUT/PATCH in postgresql.
    """
    # Selects all the students from the database and filter the student with
    # matching ID
    statement = db.select(Student).where(Student.student_id == student_id)
    student = db.session.scalar(statement)

    # Update the student information in the students database if they exist
    if student:
        # Fetch the student information from the request body
        bodyData = request.get_json()

        # Update the student's details with these new changes, otherwise 
        # reuse the same information
        student.first_name = bodyData.get("first_name", student.first_name)
        student.last_name = bodyData.get("last_name", student.last_name)
        student.email = bodyData.get("email", student.email)
        student.phone = bodyData.get("phone", student.phone)
        student.address = bodyData.get("address", student.address)
        
        # Commit and permanently update the student data in the 
        # postgresql database
        db.session.commit()

        # Return the updated student info in JSON format
        return jsonify(student_schema.dump(student))
    else:
        # Return an error message: Student with this ID does not exist
        return error_student_does_not_exist(student_id)
