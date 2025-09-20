from flask import Flask
from init import db
import os
from controllers.cli_controller import db_commands
from controllers.student_controller import student_bp
# from dotenv import load_dotenv
# load_dotenv()

def create_app():
    app = Flask(__name__)
    print("Flask server started.")
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI") # requires load_dotenv()
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")
    db.init_app(app)
    app.register_blueprint(db_commands)
    app.register_blueprint(student_bp)
    return app