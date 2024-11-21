from flask import Blueprint

instructor_blueprint = Blueprint('instructor', __name__)

from app.instructor import instructor_routes