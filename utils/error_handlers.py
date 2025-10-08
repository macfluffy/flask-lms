"""
This file is a template of all the commonly occuring errors when users input
something that would cause the API to crash, from violating the constraints 
in the schema or the expected data types of the models to meeting the data 
types but failing the validation barriers placed in the schemas. This 
function also reports the errors in a legible manner to narrow down where
failures occur.
"""

# Imported libraries
from flask import jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, DataError
from psycopg2 import errorcodes


def register_error_handlers(app):
    """
    This function defines all the typical user inputs that cause the application to
    crash. These errors will be attached to the flask app when this function is
    called in the main.py.
    """
    @app.errorhandler(ValidationError)
    def handle_validation_error(err):
        """
        This function throws a validation error message whenever a user inputs
        a value that fails to meet the validation/authentication requirements 
        placed on the models in their respective schemas.
        """
        return jsonify(err.messages), 404
    
    @app.errorhandler(IntegrityError)
    def handle_integrity_error(err):
        """
        This function throws an integrity error message whenever a user inputs
        a value that defies the table column constraints as defined in the 
        models and their schemas.
        """
        if hasattr(err, "orig") and err.orig:
            # Throw error code 23502: Not Null Violation when a user enters a 
            # null value to an attribute with a not null constraint
            if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
                return {
                    "message": 
                    f"Required field: {err.orig.diag.column_name} cannot be null."
                }, 409
            
            # Throw a unique violation message if a user enters a value that matches 
            # one already existing in this column in the respective table
            if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
                return {
                    "message": 
                    err.orig.diag.message_detail
                }, 409
            
            # Throw a foreign key violation message if a user enters a value in place 
            # of the foreign keys that does not exist in its primary table
            if err.orig.pgcode == errorcodes.FOREIGN_KEY_VIOLATION:
                return {
                    "message": 
                    err.orig.diag.message_detail
                }, 409
            
            # Throw a generic integrity error message, if a user has entered an 
            # erroneous value that falls under the integrity error but is not 
            # defined by the common error codes   
            else:
                return {
                    "message": 
                    "Unknown integrity error occured."
                }, 409
        
        # # Throw a generic integrity error message, if a user has entered an 
        # erroneous value that falls under the integrity error but there is 
        # no error code 
        else:
            return  {
                "message": 
                "Integrity Error occured."
            }, 409
        
    @app.errorhandler(DataError)
    def handle_data_error(err):
        """
        This function throws a data error message whenever a user inputs
        a value out of range in that column.
        """
        return {
            "message": 
            f"{err.orig.diag.message_primary}"
        }, 409
    
    @app.errorhandler(404)
    def handle_404(err):
        """
        This function throws a 404 error message when the page or route
        cannot be found.
        """
        return {
            "message": 
            "Requested resource not found/ does not exist"
        }, 404
    
    @app.errorhandler(500)
    def handle_server_related_error(err):
        """
        This function throws a 500 error message when there is something
        wrong on the server side. This may not return an error message if
        the server itself is down.
        """
        return {
            "message": 
            "Server error occured. Please contact the site administration."
        }, 500