from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.enrolment import Enrolment
from schemas.schemas import enrolment_schema, enrolments_schema

enrolments_bp = Blueprint("enrolments", __name__, url_prefix = "/enrolments")

def error_empty_table():
    return {"message": "No records found. Add a statement to get started."}, 404

def error_enrolment_does_not_exist(enrolment_id):
    return {"message": f"Enrolment with id {enrolment_id} does not exist"}, 404

def enrolment_sucessfully_delete(enrolment_id):
    return {"message": f"Enrolment {enrolment_id} deleted successfully."}, 200 

# Read all
@enrolments_bp.route("/")
def get_enrolments():
    enrolment_id = request.args.get("enrolment_id", type = int)
    student_id = request.args.get("student_id", type = int)
    stmt = db.select(Enrolment)
    
    if enrolment_id:
        stmt = stmt.where(Enrolment.id == enrolment_id)
    
    if student_id:
        stmt = stmt.where(Enrolment.student_id == student_id)
        # stmt = stmt.filter_by(Student.student_id == student_id)

    enrolments_list = db.session.scalars(stmt)
    queryData = enrolments_schema.dump(enrolments_list)
    if queryData:
        return jsonify(queryData)
    else:
        return error_empty_table()
    
@enrolments_bp.route("/", methods = ["POST"])
def create_enrolment():
    try:
        # Get the data from the Request Body
        bodyData = request.get_json()
        # Create a enrolment instance
        newEnrolment = Enrolment(
            enrolment_date = bodyData.get("enrolment_date"),
            student_id = bodyData.get("student_id"),
            course_id = bodyData.get("course_id")
        )
        # Add to the session
        db.session.add(newEnrolment)
        # commit it
        db.session.commit()
        # return the response
        return jsonify(enrolment_schema.dump(newEnrolment)), 201
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
    
# DELETE a enrolment - DELETE /enrolment_id
@enrolments_bp.route("/<int:enrolment_id>", methods = ["DELETE"])
def delete_enrolment(enrolment_id):
    # Find the enrolment
    # define the statement
    stmt = db.select(Enrolment).where(Enrolment.id == enrolment_id)
    # stmt = db.select(Enrolment).filter_by(enrolment_id = enrolment_id)
    # execute it
    enrolment = db.session.scalar(stmt)
    queryData = enrolment_schema.dump(enrolment)
    # If the enrolment exists
    if queryData:
        # delete it
        db.session.delete(enrolment)
        db.session.commit()
        # return message
        return enrolment_sucessfully_delete(enrolment_id)
    # else
    else:
        # acknowledge
        return error_enrolment_does_not_exist(enrolment_id)