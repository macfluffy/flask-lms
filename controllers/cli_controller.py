from flask import Blueprint
from init import db
from models.student import Student

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created.")

@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped.")

@db_commands.cli.command("seed")
def seed_tables():
    # Create an instance of the model
    students = [Student(
        name = "Alice",
        email = "alice@email.com",
        address = "Sydney"
    ), Student(
        name = "Bob",
        email = "bob@email.com"
    )]

    # Add to the session
    db.session.add_all(students)
    # Commit to the session
    db.session.commit()
    print("Tables created.")