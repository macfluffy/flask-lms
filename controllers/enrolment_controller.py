from flask import Blueprint, jsonify, request

from init import db
from models.enrolment import Enrolment
from schemas.schemas import enrolment_schema, enrolments_schema

enrolments_bp = Blueprint("enrolments", __name__, url_prefix = "/enrolments")

def error_empty_table():
    return {"message": "No records found. Add a statement to get started."}, 404

# Read all
@enrolments_bp.route("/")
def get_enrolments():
    course_id = request.args.get("course_id", type = int)
    student_id = request.args.get("student_id", type = int)
    stmt = db.select(Enrolment)
    
    if course_id:
        stmt = stmt.where(Enrolment.course_id == course_id)
    
    if student_id:
        stmt = stmt.where(Enrolment.student_id == student_id)
        # stmt = stmt.filter_by(Student.student_id == student_id)

    enrolments_list = db.session.scalars(stmt)
    queryData = enrolments_schema.dump(enrolments_list)
    if queryData:
        return jsonify(queryData)
    else:
        return error_empty_table()