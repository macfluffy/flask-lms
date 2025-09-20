from flask import Blueprint

student_bp = Blueprint("students", __name__, url_prefix = "/students")

# Routes to be defined
# GET /
# GET /id
# POST /
# PUT/PATCH /id
# DELETE /id