from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, FloatField, DecimalField
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import  ValidationError, DataRequired, EqualTo, Email, Length, NumberRange
from wtforms.widgets import ListWidget, CheckboxInput
from flask import redirect
from app.main.models import User, Instructor, Course
from app import db
import sqlalchemy as sqla
import re

def is_unique(field_name):
    if field_name == 'username':
        def _is_unique_username(form, field):
            user = db.session.scalars(sqla.select(User).where(User.username == field.data)).first()
            if user is not None:
                # return redirect('auth.login')
                raise ValidationError(message="There is already an account with that username")
        return _is_unique_username
    elif field_name == 'id':
        def _is_unique_id(form, field):
            user = db.session.scalars(sqla.select(User).where(User.id == field.data)).first()
            if user is not None:
                # return redirect('auth.login')
                raise ValidationError(message="There is already an account with that ID")
        return _is_unique_id
    
def validate_phone(form, field):
    input_number = field.data
    if re.search("[a-z]", input_number) != None:
        raise ValidationError(message="Not a valid phone number")     
    
def validate_major(form, field):
    input_number = field.data
    if re.search("[a-z]", input_number) is None:
        raise ValidationError(message="Not a valid major")  

class LoginForm(FlaskForm):
    email = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember_me = BooleanField('Remember me?')
    submit = SubmitField('Sign In')

class StudentRegistrationForm(FlaskForm):
    username = StringField('Email', validators=[DataRequired('Error, must enter a value'), Email(), is_unique('username')])
    firstname = StringField('First Name', validators=[DataRequired('Error, must enter a value')])
    lastname = StringField('Last Name', validators=[DataRequired('Error, must enter a value')])
    WPI_id = StringField('WPI ID', validators=[DataRequired('Error, must enter a value'), is_unique('id'), Length(min=9,max=9)])
    phonenumber = StringField('Phone Number', validators=[DataRequired(), Length(min=9,max=10), validate_phone])
    major = StringField('Major', validators=[DataRequired(), validate_major])
    gpa = DecimalField('GPA', validators=[DataRequired(), NumberRange(min=0,max=4.0)])
    graduation_date = StringField('Graduation Date', validators=[DataRequired(), Length(min=8, max=15, message='Must be in the format of May 2024')])

    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class InstructorRegistrationForm(FlaskForm):
    username = StringField('Email', validators=[DataRequired('Error, must enter a value'), Email(), is_unique('username')])
    firstname = StringField('First Name', validators=[DataRequired('Error, must enter a value')])
    lastname = StringField('Last Name', validators=[DataRequired('Error, must enter a value')])
    WPI_id = StringField('WPI ID', validators=[DataRequired(), is_unique('id'), Length(min=9,max=9)])
    title = StringField('Title', validators=[DataRequired()])
    phonenumber = StringField('Phone Number', validators=[DataRequired(), Length(min=9,max=10), validate_phone])
    
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
