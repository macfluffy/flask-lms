from flask import Blueprint, jsonify
from init import db
from models.student import Student, student_schema, students_schema

student_bp = Blueprint("students", __name__, url_prefix = "/students")

def error_empty_table():
    return {"message": "No records found. Add a statement to get started."}

def error_student_does_not_exist(student_id):
    return {"message": f"Student with id {student_id} does not exist"}

# Routes to be defined
# GET /
@student_bp.route("/")
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
@student_bp.route("/<int:student_id>")
def get_a_student(student_id):
    stmt = db.select(Student).where(student.student_id == student_id)
    student = db.session.scalar(stmt)
    queryData = student_schema.dump(student)
    if queryData:
        return jsonify(queryData)
    else:
        return error_student_does_not_exist(student_id)

# POST /
# PUT/PATCH /id
# DELETE /id