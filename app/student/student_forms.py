from flask_wtf import FlaskForm
from flask_login import current_user
from app import db
import sqlalchemy as sqla

from app.main.models import User, Instructor, Course, Section
from wtforms import StringField, SubmitField, PasswordField, IntegerField, FloatField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from wtforms.widgets import ListWidget, CheckboxInput

class EditStudentProfileForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired('Error, must enter a value')])
    lastname = StringField('Last Name', validators=[DataRequired('Error, must enter a value')])
    phonenumber = StringField('Phone Number', validators=[DataRequired()])
    major = StringField('Major', validators=[DataRequired()])
    gpa = FloatField('GPA', validators=[DataRequired()])
    graduation_date = StringField('Graduation Date', validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')