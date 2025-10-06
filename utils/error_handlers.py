"""
A template of all the common occuring errors
"""

# Imported libraries
from flask import jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, DataError
from psycopg2 import errorcodes

def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(err):
        return jsonify(err.messages), 404
    
    @app.errorhandler(IntegrityError)
    def handle_integrity_error(err):
        if hasattr(err, "orig") and err.orig:
            # err.orig.pgcode 23502: Not Null Violation
            if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
                return {"message": f"Required field: {err.orig.diag.column_name} cannot be null."}, 409
            
            # unique violation
            if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
                return {"message": err.orig.diag.message_detail}, 409
            
            # foreign key violation
            if err.orig.pgcode == errorcodes.FOREIGN_KEY_VIOLATION:
                return {"message": err.orig.diag.message_detail}, 409
            
            else:
                return {"message": "Unknown integrity error occured."}, 409
            
        else:
            return  {"message": "Integrity Error occured."}, 409
        
    @app.errorhandler(DataError)
    def handle_data_error(err):
        return {"message": f"{err.orig.diag.message_primary}"}, 409
    
    @app.errorhandler(404)
    def handle_404(err):
        return {"message": "Requested resource not found/ does not exist"}, 404
    
    @app.errorhandler(500)
    def handle_server_related_error(err):
        return {"message": "Server error occured. Please contact the site administration."}, 500