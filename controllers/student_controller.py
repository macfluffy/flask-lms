from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.student import Student
from schemas.schemas import student_schema, students_schema

students_bp = Blueprint("students", __name__, url_prefix = "/students")

def error_empty_table():
    return {"message": "No records found. Add a statement to get started."}

def error_student_does_not_exist(student_id):
    return {"message": f"Student with id {student_id} does not exist"}, 404

# Routes to be defined
# GET /
@students_bp.route("/")
def get_students():
    # Define a statement: SELECT * FROM students;
    stmt = db.select(Student)
    # Execute it
    students_list = db.session.scalars(stmt)
    # Serialise it
    queryData = students_schema.dump(students_list)
    print("The name of the students:", {student["name"] for student in queryData})
    if queryData:
        # Return the jsonify(list)
        return jsonify(queryData)
    else:
        return error_empty_table()

# GET /id
@students_bp.route("/<int:student_id>")
def get_a_student(student_id):
    stmt = db.select(Student).where(Student.student_id == student_id)
    student = db.session.scalar(stmt)
    queryData = student_schema.dump(student)
    if queryData:
        return jsonify(queryData)
    else:
        return error_student_does_not_exist(student_id)

# POST /
@students_bp.route("/", methods = ["POST"])
def create_student():
    try:
        # GET details from the REQUEST body
        bodyData = request.get_json()
        # email = bodyData.get("email")
        # stmt = db.select(Student).where(Student.email == email)
        # student = db.session.scalar(stmt)
        # data = student_schema.dump(student)
        # if data:
            # return {"message": f"The Student with email:{email} already exists."}, 409
        
        # Create a student object with the request body data
        newStudent = Student(
            name = bodyData.get("name"),
            email = bodyData.get("email"),
            address = bodyData.get("address")
        )
        # Add to the session
        db.session.add(newStudent)
        # Commit the session
        db.session.commit()
        # Send acknowledgement
        acknowledgement = student_schema.dump(newStudent)
        return jsonify(acknowledgement), 201
    except IntegrityError as err:
        # if int(err.orig.pgcode) == 23502: # not null violation
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION: # not null violation
            return {"message": f"Required field: {err.orig.diag.column_name} cannot be null."}, 409
        
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION: # unique violation
            return {"message": err.orig.diag.message_detail}, 409
        
        else:
            return  {"message": "Integrity Error occured."}, 409
    except:
        return {"message": "Unexpected error occured."}, 400

# DELETE /id
@students_bp.route("/<int:student_id>", methods = ["DELETE"])
def delete_student(student_id):
    # find the student with id
    stmt = db.select(Student).where(Student.student_id == student_id)
    student = db.session.scalar(stmt)
    # if student exists
    if student:
        # delete
        db.session.delete(student)
        # commit
        db.session.commit()
        # return ack
        return {"message": f"Student {student.name} deleted successfully."}, 200 
    # else
    else:
        # return ack
        return {"message": f"Student with id: {student_id} does not exist."}, 404

# PUT/PATCH /id
@students_bp.route("/<int:student_id>", methods = ["PUT", "PATCH"])
def update_student(student_id):
    try:
        # Get the student from the database
        # define the stmt
        stmt = db.select(Student).where(Student.student_id == student_id)
        # execute the statement
        student = db.session.scalar(stmt)
        # if the student exists
        if student:
            # fetch the info from the request body
            bodyData = request.get_json()
            # make the changes, short circuit method
            student.name = bodyData.get("name", student.name)
            student.email = bodyData.get("email", student.email)
            student.address = bodyData.get("address", student.address)
            # commit to the db
            db.session.commit()
            # ack
            return jsonify(student_schema.dump(student))
        # else
        else:
            # ack message
            return error_student_does_not_exist(student_id)
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION: # unique violation
            return {"message": err.orig.diag.message_detail}, 409