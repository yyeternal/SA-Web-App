from app import db
from app.main import main_blueprint as bp_main
from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.instructor.instructor_forms import CourseSectionForm, CreatePositionForm
from app.main.models import Section, SA_Position
from flask_login import login_required
import sqlalchemy as sqla

@bp_main.route('/', methods=['GET'])
@bp_main.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('index.html', title='SA Recruitment Web App')