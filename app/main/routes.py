from app import db
from app.main import main_blueprint as bp_main
from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_login import login_required
import sqlalchemy as sqla
import os
from app.auth.auth_routes import authent

@bp_main.route('/', methods=['GET'])
@bp_main.route('/index', methods=['GET'])
@login_required
def index():
    if current_user.user_type == "Student":
        return redirect(url_for('student.view_positions'))
    if current_user.user_type == "Instructor":
        return redirect(url_for('instructor.view_positions'))
    return render_template('index.html', title='SA Recruitment Web App')