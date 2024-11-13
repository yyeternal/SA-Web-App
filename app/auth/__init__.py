from flask import Blueprint

auth_bluprint = Blueprint('auth', __name__)

from app.auth import auth_routes

