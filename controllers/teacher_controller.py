from flask import Blueprint, jsonify, request
from init import db
from models.teacher import Teacher, teacher_schema, teachers_schema
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

teachers_bp = Blueprint("teachers", __name__, url_prefix = "/teachers")

def error_empty_table():
    return {"message": "No records found. Add a statement to get started."}, 404

def error_teacher_does_not_exist(teacher_id):
    return {"message": f"Teacher with id {teacher_id} does not exist"}, 404

# CREATE - POST /
@teachers_bp.route("/", methods = ["POST"])
def create_teacher():
    try:
        # GET details from the REQUEST body
        bodyData = request.get_json()
        # department = bodyData.get("department")
        # stmt = db.select(Teacher).where(Teacher.department == department)
        # teacher = db.session.scalar(stmt)
        # data = teacher_schema.dump(teacher)
        # if data:
            # return {"message": f"The Teacher with department:{department} already exists."}, 409
        
        # Create a teacher object with the request body data
        newTeacher = Teacher(
            name = bodyData.get("name"),
            department = bodyData.get("department"),
            address = bodyData.get("address")
        )
        # Add to the session
        db.session.add(newTeacher)
        # Commit the session
        db.session.commit()
        # Send acknowledgement
        acknowledgement = teacher_schema.dump(newTeacher)
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
        return {"message": "Unexpected error occured."}
    
# READ - GET / AND /id
@teachers_bp.route("/")
def get_teachers():
    # Define the statement for GET ALL teachers: SELECT * FROM teachers;
    stmt = db.Select(Teacher)
    # Execute it
    teachers_list = db.session.scalars(stmt)
    queryData = teachers_schema.dump(teachers_list)
    # if it exists:
    if queryData:
        # return it
        return jsonify(queryData)
    # else:
    else:
        # acknowledgement message
        return error_empty_table()

@teachers_bp.route("/<int:teacher_id>")
def get_a_teacher(teacher_id):
    # Define the statement for GET ALL teachers: SELECT * FROM teachers WHERE id = teacher_id;
    stmt = db.Select(Teacher).where(Teacher.teacher_id == teacher_id)
    # Execute it
    teachers_list = db.session.scalar(stmt)
    queryData = teacher_schema.dump(teachers_list)
    # if it exists:
    if queryData:
        # return it
        return jsonify(queryData)
    # else:
    else:
        # acknowledgement message
        return error_teacher_does_not_exist(teacher_id)

# UPDATE - PUT/PATCH /id
# DELETE - DELETE /id
@teachers_bp.route("/<int:teacher_id>", methods = ["DELETE"])
def delete_teacher(teacher_id):
    # find the teacher with id
    stmt = db.select(Teacher).where(Teacher.teacher_id == teacher_id)
    teacher = db.session.scalar(stmt)
    # if teacher exists
    if teacher:
        # delete
        db.session.delete(teacher)
        # commit
        db.session.commit()
        # return ack
        return {"message": f"Teacher {teacher.name} deleted successfully."}, 200 
    # else
    else:
        # return ack
        return {"message": f"Teacher with id: {teacher_id} does not exist."}, 404