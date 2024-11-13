from flask import Blueprint

main_bluprint = Blueprint('main', __name__)

from app.main import routes