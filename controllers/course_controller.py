from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.course import Course
from schemas.schemas import course_schema, courses_schema

courses_bp = Blueprint("courses", __name__, url_prefix = "/courses")

def error_empty_table():
    return {"message": "No records found. Add a statement to get started."}, 404

def error_course_does_not_exist(course_id):
    return {"message": f"Course with id {course_id} does not exist"}, 404

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
@courses_bp.route("/<int:course_id>")
def get_a_course(course_id):
    # Define the statement
    # SQL: SELECT * FROM courses WHERE course_id = course_id;
    stmt = db.select(Course).where(Course.course_id == course_id)
    # execute it
    course = db.session.scalar(stmt)
    # serialise it
    queryData = course_schema.dump(course)
    # if the course exists
    if queryData:
        # return it
        return jsonify(queryData)
    # else
    else:
        # acknowledge
        return error_course_does_not_exist(course_id)
    
# CREATE - POST /
@courses_bp.route("/", methods = ["POST"])
def create_course():
    try:
        # Get the data from the Request Body
        bodyData = request.get_json()
        # Create a course instance
        newCourse = Course(
            name = bodyData.get("name"),
            duration = bodyData.get("duration"),
            teacher_id = bodyData.get("teacher_id")
        )
        # Add to the session
        db.session.add(newCourse)
        # commit it
        db.session.commit()
        # return the response
        return jsonify(course_schema.dump(newCourse)), 201
    except IntegrityError as err:
        # if int(err.orig.pgcode) == 23502: # not null violation
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION: # not null violation
            return {"message": f"Required field: {err.orig.diag.column_name} cannot be null."}, 409
        
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION: # unique violation
            return {"message": err.orig.diag.message_detail}, 409
        
        if err.orig.pgcode == errorcodes.FOREIGN_KEY_VIOLATION: # foreign key violation
            return {"message": err.orig.diag.message_detail}, 409
        
        else:
            return  {"message": "Integrity Error occured."}, 409
    except:
        return {"message": "Unexpected error occured."}, 400

# DELETE a course - DELETE /course_id
# UPDATE - PUT/PATCH /course_id