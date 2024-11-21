from app import db
from app.student import student_blueprint as bp_student
from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.main.models import Section, SA_Position
from flask_login import login_required
import sqlalchemy as sqla

@bp_student.route('/positions/view', methods=['GET'])
@login_required
def view_positions():
    return render_template('student.html')