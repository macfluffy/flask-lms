"""
This file creates the Create, Read, Update, and Delete operations to the teacher data,
through REST API design using Flask Blueprint.
"""

# Installed import packages
from flask import Blueprint, jsonify, request

# Local imports
from init import db
from models.teacher import Teacher
from schemas.schemas import teacher_schema, teachers_schema


# Create the Template Web Application Interface for teachers routes to be applied 
# to the Flask application
teachers_bp = Blueprint("teachers", __name__, url_prefix = "/teachers")


"""
Teacher Controller Messages
"""

def error_empty_table():
    return {"message": "No records found. Add a statement to get started."}, 404

def error_teacher_does_not_exist(teacher_id):
    return {"message": f"Teacher with id {teacher_id} does not exist"}, 404

def teacher_successfully_removed(first_name, last_name):
    return {"message": f"Teacher {first_name} {last_name} deleted successfully."}, 200 


"""
API Routes
"""

@teachers_bp.route("/", methods = ["POST"])
def create_teacher():
    """
    Retrieve and read all the teachers from the teachers database,
    this is the equivalent of GET in postgresql.
    """
    # Fetch the enrolment information from the request body
    bodyData = request.get_json()

    # Create a new enrolment object using the request body data and the enrolment schema
    # will organise the data to their matching attributes with validation rules 
    # implemented
    newTeacher = teacher_schema.load(
        bodyData,
        session = db.session
    )

    # Add the new teacher information to the session
    db.session.add(newTeacher)

    # Commit and write the teacher data from this session into 
    # the postgresql database
    db.session.commit()
    acknowledgement = teacher_schema.dump(newTeacher)
    return jsonify(acknowledgement), 201

    
@teachers_bp.route("/")
def get_teachers():
    """
    Retrieve and read all the teachers from the teachers database,
    this is the equivalent of GET in postgresql.
    """
    # Check for filter requests by department name from the URL
    department = request.args.get("department")

    # Display teachers within the queried department
    if department:
        statement = db.select(Teacher).where(Teacher.department == department)
    else:    
        # Select all teachers in the database
        statement = db.Select(Teacher)

    # Serialise it as the scalar result is unserialised
    teachers_list = db.session.scalars(statement)
    queryData = teachers_schema.dump(teachers_list)

    # Return the search results if there are teachers in the teacher database, 
    # otherwise inform the user that the database is empty.
    if queryData:
        # Return the list of teachers in JSON format
        return jsonify(queryData)
    # else:
    else:
        # Return an error message: Teachers table is empty
        return error_empty_table()


@teachers_bp.route("/<int:teacher_id>")
def get_a_teacher(teacher_id):
    """
    Retrieve and read a specific teacher's information from 
    the teacher database, using the teacher ID as the marker.
    """
    # Selects all the teachers from the database and filter the teacher with
    # matching ID
    statement = db.Select(Teacher).where(Teacher.teacher_id == teacher_id)
    teachers_list = db.session.scalar(statement)

    # Serialise it as the scalar result is unserialised
    queryData = teacher_schema.dump(teachers_list)
    
    # Return the search results if this teachers is in the teacher database, 
    # otherwise inform the user that this teacher does not exist.
    if queryData:
        # Return the list of teachers in JSON format
        return jsonify(queryData)
    # else:
    else:
        # Return an error message: Teacher with this ID does not exist
        return error_teacher_does_not_exist(teacher_id)


@teachers_bp.route("/<int:teacher_id>", methods = ["PUT", "PATCH"])
def update_teacher(teacher_id):
    """
    Retrieve the body data and update the details of the teacher with the 
    matching ID in the teacher database, this is the equivalent of 
    PUT/PATCH in postgresql.
    """
    # Selects all the teachers from the database and filter the teacher with
    # matching ID
    statement = db.select(Teacher).where(Teacher.teacher_id == teacher_id)
    teacher = db.session.scalar(statement)

    # Update the teacher information in the teachers database if they exist
    if teacher:
        # Fetch the teacher information from the request body
        bodyData = request.get_json()

        # Update the teacher's details with these new changes, otherwise 
        # reuse the same information
        teacher.first_name = bodyData.get("first_name", teacher.first_name)
        teacher.last_name = bodyData.get("last_name", teacher.last_name)
        teacher.department = bodyData.get("department", teacher.department)
        teacher.address = bodyData.get("address", teacher.address)
        teacher.phone = bodyData.get("phone", teacher.phone)
        teacher.email = bodyData.get("email", teacher.email)

        # Commit and permanently update the teacher data in the 
        # postgresql database
        db.session.commit()

        # Return the updated teacher info in JSON format
        return jsonify(teacher_schema.dump(teacher))
    else:
        # Return an error message: Teacher with this ID does not exist
        return error_teacher_does_not_exist(teacher_id)

        
@teachers_bp.route("/<int:teacher_id>", methods = ["DELETE"])
def delete_teacher(teacher_id):
    """
    Find the teacher with the matching ID in the teacher database and remove it.
    This is the equivalent of DELETE in postgresql.
    """
    # Selects all the teachers from the database and filter the teacher with
    # matching ID
    statement = db.select(Teacher).where(Teacher.teacher_id == teacher_id)
    teacher = db.session.scalar(statement)

    # Delete the teacher from the teachers database if they exist
    if teacher:
        # Remove the teacher from the session
        db.session.delete(teacher)
        # Commit and permanently remove the teacher data from the 
        # postgresql database
        db.session.commit()
        
        # Return an acknowledgement
        return teacher_successfully_removed(teacher.first_name, teacher.last_name)
    else:
        # Return an error message: Teacher with this ID does not exist
        return error_teacher_does_not_exist(teacher_id)