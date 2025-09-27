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

load_dotenv()

def create_app():
    app = Flask(__name__)
    print("Flask server started.")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI") # requires load_dotenv()
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")
    # Keep the order of keys in JSON response
    app.json.sort_keys = False
    db.init_app(app)
    app.register_blueprint(db_commands)
    app.register_blueprint(students_bp)
    app.register_blueprint(teachers_bp)
    app.register_blueprint(courses_bp)
    return app