"""
This file creates the Create, Read, Update, and Delete operations to the enrolment data,
through REST API design using Flask Blueprint.
"""

# Installed import packages
from flask import Blueprint, jsonify, request

# Local imports
from init import db
from models.enrolment import Enrolment
from schemas.schemas import enrolment_schema, enrolments_schema


# Create the Template Web Application Interface for enrolments routes to be applied 
# to the Flask application
enrolments_bp = Blueprint("enrolments", __name__, url_prefix = "/enrolments")


"""
Enrolment Controller Error Messages
"""

def error_empty_table():
    return {"message": "No records found. Add a statement to get started."}, 404

def error_enrolment_does_not_exist(enrolment_id):
    return {"message": f"Enrolment with id {enrolment_id} does not exist"}, 404

def enrolment_sucessfully_delete(enrolment_id):
    return {"message": f"Enrolment {enrolment_id} deleted successfully."}, 200 


"""
API Routes
"""

@enrolments_bp.route("/")
def get_enrolments():
    """
    Retrieve and read all the enrolments from the enrolments database,
    this is the equivalent of GET in postgresql.
    """
    # Select all the enrolments from the database and the students that
    # are enrolled in these courses
    enrolment_id = request.args.get("enrolment_id", type = int)
    student_id = request.args.get("student_id", type = int)
    statement = db.select(Enrolment)
    
    # Display enrolments that exist
    if enrolment_id:
        statement = statement.where(Enrolment.id == enrolment_id)
    
    # Display students that exist in the enrolment
    if student_id:
        statement = statement.where(Enrolment.student_id == student_id)

    # Serialise it as the scalar result is unserialised
    enrolments_list = db.session.scalars(statement)
    queryData = enrolments_schema.dump(enrolments_list)

    # Return the search results if there are enrolments in the enrolment database, 
    # otherwise inform the user that the database is empty.
    if queryData:
        # Return the list of enrolments in JSON format
        return jsonify(queryData)
    else:
        # Return an error message: Enrolments table is empty
        return error_empty_table()


@enrolments_bp.route("/", methods = ["POST"])
def create_enrolment():
    """
    Retrieve the body data and add the details of the enrolment into the enrolment database,
    this is the equivalent of POST in postgresql.
    """
    # try:
    # Fetch the enrolment information from the request body
    bodyData = request.get_json()

    # Create a new enrolment object using the request body data and the enrolment schema
    # will organise the data to their matching attributes
    newEnrolment = Enrolment(
        enrolment_date = bodyData.get("enrolment_date"),
        student_id = bodyData.get("student_id"),
        course_id = bodyData.get("course_id")
    )
    
    # Add the enrolment data into the session
    db.session.add(newEnrolment)
    
    # Commit and write the enrolment data from this session into 
    # the postgresql database
    db.session.commit()
    return jsonify(enrolment_schema.dump(newEnrolment)), 201
    

@enrolments_bp.route("/<int:enrolment_id>", methods = ["DELETE"])
def delete_enrolment(enrolment_id):
    """
    Find the enrolment with the matching ID in the enrolment database and remove it.
    This is the equivalent of DELETE in postgresql.
    """
    # Selects all the enrolments from the database and filter the enrolment with
    # matching ID
    statement = db.select(Enrolment).where(Enrolment.id == enrolment_id)
    
    # Serialise it as the scalar result is unserialised
    enrolment = db.session.scalar(statement)
    queryData = enrolment_schema.dump(enrolment)

    # Delete the enrolment from the enrolments database if they exist
    if queryData:
        # Remove the enrolment from the session
        db.session.delete(enrolment)
        
        # Commit and permanently remove the enrolment data from the 
        # postgresql database
        db.session.commit()
        
        # Return an acknowledgement
        return enrolment_sucessfully_delete(enrolment_id)
    else:
        # Return an error message: Enrolment with this ID does not exist
        return error_enrolment_does_not_exist(enrolment_id)