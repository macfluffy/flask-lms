"""
Using app factory design method for handling 
"""

# Built-in imports
import os

# Installed import packages
from flask import Flask
from dotenv import load_dotenv

# Local imports
from init import db
from controllers.cli_controller import db_commands
from controllers.student_controller import students_bp
from controllers.teacher_controller import teachers_bp
from controllers.course_controller import courses_bp
from controllers.enrolment_controller import enrolments_bp
from utils.error_handlers import register_error_handlers

load_dotenv()

# Create a single instance of the Flask application which will be called from the rest of the code
def create_app():
    app = Flask(__name__)
    print("Flask server started.")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI") # requires load_dotenv()
    
    # Keep the order of keys in JSON response
    app.json.sort_keys = False
    db.init_app(app)

    # Apply the imported routes created in the controllers folder to this instance of Flask app
    app.register_blueprint(db_commands)
    app.register_blueprint(students_bp)
    app.register_blueprint(teachers_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(enrolments_bp)

    # Apply the imported error handling created in the utilities folder to this Flask app instance
    register_error_handlers(app)
    return app