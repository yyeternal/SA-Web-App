from flask_wtf import FlaskForm
from flask_login import current_user
from app import db
import sqlalchemy as sqla

from app.main.models import User, Instructor, Course
from wtforms import StringField, SubmitField, PasswordField, IntegerField, FloatField, DecimalField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, NumberRange, AnyOf
from wtforms.widgets import ListWidget, CheckboxInput
import re

def validate_phone(form, field):
    input_number = field.data
    if re.search("[a-z]", input_number) != None:
        raise ValidationError(message="Not a valid phone number")  

def validate_course_num(form, field):
    input_num = field.data
    courses = db.session.scalars(sqla.select(Course)).all()
    for course in courses:
        if input_num == course.coursenum:
            raise ValidationError(message="This section already exists!") 

class CreatePositionForm(FlaskForm):
    course = QuerySelectField('Course',
                         query_factory= lambda : db.session.scalars(sqla.select(Course)),
                         get_label= lambda c : '{} - {}'.format(c.coursenum, c.title))
    sectionnum = StringField('Section Number', validators=[DataRequired(), Length(min=1, max=10), validate_course_num])
    term = StringField('Enter the term for the class. e.g. "A 2023"', validators=[DataRequired(), Length(min=6, max=6, message='Must be in the format of A 2024')])
    open_positions = IntegerField('Number of Positions', validators=[DataRequired(), NumberRange(min=1)])
    min_GPA = DecimalField('Minimum GPA of SA', validators=[DataRequired(), NumberRange(min=0,max=4.0)])
    min_grade = StringField('Minimum Grade of SA', validators=[DataRequired(), AnyOf(values=['A', 'B', 'C'], message="Must be A, B, or C")])
    submit = SubmitField('Create')


class EditInstructorProfileForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired('Error, must enter a value')])
    lastname = StringField('Last Name', validators=[DataRequired('Error, must enter a value')])
    title = StringField('Title', validators=[DataRequired()])
    phonenumber = StringField('Phone Number', validators=[DataRequired(), Length(min=9,max=10), validate_phone])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')