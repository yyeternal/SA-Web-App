from app import db
from app.student import student_blueprint as bp_student
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.main.models import Section, SA_Position
from app.student.student_forms import EditStudentProfileForm
from flask_login import login_required
import sqlalchemy as sqla

@bp_student.route('/positions/view', methods=['GET'])
@login_required
def view_positions():
    return render_template('student.html')

@bp_student.route('/student/edit', methods=['GET', 'POST'])
@login_required
def edit_student_profile():
    if not current_user.user_type == 'Student':
        flash('You do not have access to this page')
        return redirect(url_for('main.index'))
    sform = EditStudentProfileForm()
    if request.method == 'POST':
        if sform.validate_on_submit():
            current_user.firstname = sform.firstname.data
            current_user.lastname = sform.lastname.data
            current_user.phone_number = sform.phonenumber.data
            current_user.major = sform.major.data
            current_user.GPA = sform.gpa.data
            current_user.graduation_date = sform.graduation_date.data
            current_user.set_password(sform.password.data)
            db.session.commit()
            flash('Updated profile')
            return redirect(url_for('main.index'))
    elif request.method == 'GET':
        # populate form data from the DB
        sform.firstname.data = current_user.firstname
        sform.lastname.data = current_user.lastname
        sform.phonenumber.data = current_user.phone_number
        sform.major.data = current_user.major
        sform.gpa.data = current_user.GPA
        sform.graduation_date.data = current_user.graduation_date
    return render_template('student_edit_profile.html', form = sform)