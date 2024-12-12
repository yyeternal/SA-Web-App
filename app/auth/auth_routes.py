
from flask import render_template, flash, redirect, url_for, session, request

import os
from app import db
from app.auth import auth_blueprint as bp_auth 
import sqlalchemy as sqla

from app.main.models import User, Instructor, Student, Enrollment
from app.auth.auth_forms import LoginForm, InstructorRegistrationForm, StudentRegistrationForm

from flask_login import login_user, current_user, logout_user, login_required
from config import Config
import identity.web

authent = identity.web.Auth(
        session=session,
        authority=os.getenv("AUTHORITY"),
        client_id=os.getenv("CLIENT_ID"),
        client_credential=os.getenv("CLIENT_SECRET"),
    )

@bp_auth.route('/user/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    lform = LoginForm()
    if lform.validate_on_submit():
        query = sqla.select(User).where(User.username == lform.email.data)
        user = db.session.scalars(query).first()
        if (user is None) or (user.check_password(lform.password.data) == False):
            flash('Login wrong')
            return redirect(url_for('auth.login'))
        login_user(user, remember = lform.remember_me.data)
        flash('The user {} has succesfully logged in! '.format(current_user.username))

        return redirect(url_for('main.index'))
    return render_template('login.html', form = lform)

@bp_auth.route('/sso/login', methods=['GET', 'POST'])
def sso_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template("sso_login.html", **authent.log_in(
        scopes=Config.SCOPE, # Have user consent to scopes during log-in
        redirect_uri=url_for('auth.response', _external=True), # Optional. If present, this absolute URL must match your app's redirect_uri registered in Microsoft Entra admin center
        prompt="select_account",  # Optional.
        ))

@bp_auth.route('/response', methods=['GET'])
def response():
    result = authent.complete_log_in(request.args)
    if "error" in result:
        return render_template("auth_error.html", result=result)
    # print(result)
    print("Preferred username from authent.complete_log_in: {}".format(result["preferred_username"]))
    user = db.session.scalars(sqla.select(User).where(User.username == result["preferred_username"])).first()
    if user is None:
        flash("Create an account in order to SSO Login")
        return redirect(url_for('auth.choose_user'))
    login_user(user, remember=True)
    flash('The user {} has succesfully logged in! '.format(current_user.username))
    print('The user {} has succesfully logged in! '.format(current_user.username))
    return redirect(url_for('main.index'))

@bp_auth.route('/user/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@bp_auth.route('/choose_user', methods=['GET'])
def choose_user():
    return render_template('choose_user.html')

@bp_auth.route('/student/register', methods=['GET', 'POST'])
def student_register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    sform = StudentRegistrationForm()
    if sform.validate_on_submit():
        user = Student( username = sform.username.data,
                          firstname = sform.firstname.data,
                          lastname = sform.lastname.data,
                          id = sform.WPI_id.data,
                          user_type = 'Student',
                          phone_number = sform.phonenumber.data,
                          major = sform.major.data, 
                          GPA  = sform.gpa.data,
                          graduation_date = sform.graduation_date.data)    # need to finish this when we have a student model
        user.set_password(sform.password.data)
        #for c in sform.courses.data:
        #    current_user.enrollments.add(c)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login')) 
    return render_template('student_register.html', form = sform)    

@bp_auth.route('/instructor/register', methods=['GET', 'POST'])
def instructor_register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    iform = InstructorRegistrationForm()
    if iform.validate_on_submit():
        user = Instructor(username = iform.username.data,
                          firstname = iform.firstname.data,
                          lastname = iform.lastname.data,
                          id = iform.WPI_id.data,
                          user_type = 'Instructor',
                          phone_number = iform.phonenumber.data,
                          title = iform.title.data)   
        user.set_password(iform.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('instructor_register.html', form = iform)
