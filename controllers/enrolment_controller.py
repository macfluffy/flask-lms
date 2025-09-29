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
    stmt = db.select(Enrolment)
    enrolments_list = db.session.scalars(stmt)
    queryData = enrolments_schema.dump(enrolments_list)
    if queryData:
        return jsonify(queryData)
    else:
        return error_empty_table()