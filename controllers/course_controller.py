"""
This file creates the Create, Read, Update, and Delete operations to the course data,
through REST API design using Flask Blueprint.
"""

# Installed import packages
from flask import Blueprint, jsonify, request

# Local imports
from init import db
from models.course import Course
from schemas.schemas import course_schema, courses_schema


# Create the Template Web Application Interface for course routes to be applied 
# to the Flask application
courses_bp = Blueprint("courses", __name__, url_prefix = "/courses")


"""
Course Controller Messages
"""

def error_empty_table():
    return {"message": "No records found. Add a statement to get started."}, 404

def error_course_does_not_exist(course_id):
    return {"message": f"Course with id {course_id} does not exist"}, 404

def course_sucessfully_delete(course_name):
    return {"message": f"Course {course_name} deleted successfully."}, 200 


"""
API Routes
"""

@courses_bp.route("/")
def get_courses():
    """
    Retrieve and read all the courses from the course database,
    this is the equivalent of GET in postgresql.
    """
    # Selects all the courses from the database
    statement = db.select(Course)
    courses_lists = db.session.scalars(statement)
    
    # Serialise it as the scalar result is unserialised
    queryData = courses_schema.dump(courses_lists)
    
    # Return the search results if there are courses in the course database, 
    # otherwise inform the user that the database is empty.
    if queryData:
        # Return the list of courses in JSON format
        return jsonify(queryData)
    else:
        # Return an error message: Course table is empty
        return error_empty_table()


@courses_bp.route("/<int:course_id>")
def get_a_course(course_id):
    """
    Retrieve and read a specific course's information from 
    the course database, using the course ID as the marker.
    """
    # Selects all the courses from the database and filter the course with
    # matching ID
    statement = db.select(Course).where(Course.course_id == course_id)
    course = db.session.scalar(statement)
    
    # Serialise it as the scalar result is unserialised
    queryData = course_schema.dump(course)
    
    # Return the search results if this courses is in the course database, 
    # otherwise inform the user that this course does not exist.
    if queryData:
        # Return the course info in JSON format
        return jsonify(queryData)
    # else
    else:
        # Return an error message: Course with this ID does not exist
        return error_course_does_not_exist(course_id)
    

@courses_bp.route("/", methods = ["POST"])
def create_course():
    """
    Retrieve the body data and add the details of the course into the course database,
    this is the equivalent of POST in postgresql.
    """
    # Fetch the course information from the request body
    bodyData = request.get_json()
    
    # Create a new course object using the request body data and the course schema
    # will organise the data to their matching attributes with validation rules 
    # implemented
    newCourse = course_schema.load(
        bodyData,
        session = db.session
    )
    
    # Add the course data into the session
    db.session.add(newCourse)

    # Commit and write the course data from this session into 
    # the postgresql database
    db.session.commit()
    return jsonify(course_schema.dump(newCourse)), 201


@courses_bp.route("/<int:course_id>", methods = ["DELETE"])
def delete_course(course_id):
    """
    Find the course with the matching ID in the course database and remove it.
    This is the equivalent of DELETE in postgresql.
    """
    # Selects all the courses from the database and filter the course with
    # matching ID
    statement = db.select(Course).where(Course.course_id == course_id)
    course = db.session.scalar(statement)
    queryData = course_schema.dump(course)

    # Delete the course from the courses database if they exist
    if queryData:
        # Remove the course from the session
        db.session.delete(course)

        # Commit and permanently remove the course data from the 
        # postgresql database
        db.session.commit()
        
        # Return an acknowledgement
        return course_sucessfully_delete(course.name)
    else:
        # Return an error message: Course with this ID does not exist
        return error_course_does_not_exist(course_id)
    

@courses_bp.route("/<int:course_id>", methods = ["PUT", "PATCH"])
def update_a_course(course_id):
    """
    Retrieve the body data and update the details of the course with the 
    matching ID in the course database, this is the equivalent of 
    PUT/PATCH in postgresql.
    """
    # Selects all the courses from the database and filter the course with
    # matching ID
    course = db.session.get(Course, course_id)

    # Notify the user if the course doesn't exist in the database
    if not course:
        return error_course_does_not_exist(course_id)

    # Get the values to be updated from the request body
    bodyData = request.get_json()

    # Update the course information in the courses database using the request 
    # body data and the course schema will organise the data to their 
    # matching attributes with validation rules implemented
    course = course_schema.load(
        bodyData,
        instance = course,
        session = db.session,
        partial = True
    )

    # Commit and write the course data from this session into 
    # the postgresql database
    queryData = course_schema.dump(course)
    db.session.commit()
    return jsonify(queryData), 200
