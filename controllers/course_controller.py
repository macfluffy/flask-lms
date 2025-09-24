from flask import Blueprint, jsonify, request
from init import db

from models.course import Course
from schemas.schemas import course_schema, courses_schema

courses_bp = Blueprint("courses", __name__, url_prefix = "/courses")

def error_empty_table():
    return {"message": "No records found. Add a statement to get started."}, 404

# READ - GET /
@courses_bp.route("/")
def get_courses():
    # Define the statement
    stmt = db.select(Course)
    # Execute it
    courses_lists = db.session.scalars(stmt)
    # Serialise it
    queryData = courses_schema.dump(courses_lists)
    # If it exists:
    if queryData:
        # Return it
        return jsonify(queryData)
    # Else:
    else:
        #Acknowledge
        return error_empty_table()

# READ a course - GET /course_id
# CREATE - POST /
# DELETE a course - DELETE /course_id
# UPDATE - PUT/PATCH /course_id