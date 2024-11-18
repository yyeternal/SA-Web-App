<<<<<<< HEAD
from flask_wtf import FlaskForm
from app.main.models import User
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import  ValidationError, DataRequired, EqualTo, Email

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Error, must enter a value')])
    email = StringField('Email', validators= [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    validate_username(username)
    validate_email(email)
    def validate_username(self, username):
        query = sqla.select(User).where(User.username == username.data)
        user = db.session.scalars(query).first()
        if user is not None:
            raise ValidationError('Username already exists! Try another one')

    def validate_email(self, email):
        query = sqla.select(User).where(User.email == email.data)
        user = db.session.scalars(query).first()
        if user is not None:
            raise ValidationError('Email already exists! Try another one')
=======

from flask import render_template, flash, redirect, url_for

from app import db
from app.auth import auth_blueprint as bp_auth 
import sqlalchemy as sqla

from app.main.models import User
from app.auth.auth_forms import LoginForm

from flask_login import login_user, current_user, logout_user, login_required

@bp_auth.route('/user/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    lform = LoginForm()
    if lform.validate_on_submit():
        query = sqla.select(User).where(User.username == lform.username.data)
        user = db.session.scalars(query).first()
        if (user is None) or (user.check_password(lform.password.data) == False):
            flash('Login wrong')
            return redirect(url_for('auth.login'))
        login_user(user, remember = lform.remember_me.data)
        flash('The user {} has succesfully logged in! '.format(current_user.username))
        return redirect(url_for('main.index'))
    return render_template('login.html', form = lform)

>>>>>>> 93e8e17464f79f47eedbfb53cfa48b74a1d2dfb5
