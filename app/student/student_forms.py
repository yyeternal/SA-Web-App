from flask_wtf import FlaskForm
from flask_login import current_user
from app import db
import sqlalchemy as sqla

from app.main.models import User, Instructor, Course
from wtforms import StringField, SubmitField, PasswordField, IntegerField, FloatField, BooleanField, DecimalField, SelectField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, NumberRange, AnyOf
from wtforms.widgets import ListWidget, CheckboxInput
import re


class EditStudentProfileForm(FlaskForm):
    def validate_phone(form, field):
        input_number = field.data
        if re.search("[a-z]", input_number) != None:
            raise ValidationError(message="Not a valid phone number") 
        
         
    firstname = StringField('First Name', validators=[DataRequired('Error, must enter a value')])
    lastname = StringField('Last Name', validators=[DataRequired('Error, must enter a value')])
    phonenumber = StringField('Phone Number', validators=[DataRequired(), Length(min=9,max=10), validate_phone])
    major = SelectField('Major',
                         choices= ['CS', 'RBE', 'IMGD', 'DS'])
    gpa = DecimalField('GPA', validators=[DataRequired(), NumberRange(min=0,max=4.0)])
    graduation_date = StringField('Graduation Date', validators=[DataRequired(), Length(min = 6, max = 6, message='Must format in the style of A 2024 for example')])    

    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class AddCourseForm(FlaskForm):
    course = QuerySelectField('Course',
                         query_factory= lambda : db.session.scalars(sqla.select(Course)),
                         get_label= lambda c : 'CS{} - {}'.format(c.coursenum, c.title))
    wasSA = BooleanField('Were you an SA?')
    grade = StringField('Grade recieved', validators=[DataRequired(message="Please fill out this field"), AnyOf(values=['A', 'B', 'C'], message= "Must be A, B, or C")])
    term = StringField('What term and year did you take this course? Enter as term and year. e.g. "A 2023"', validators=[DataRequired(), Length(min = 6, max = 6, message='Must format in the style of A 2024 for example')])
    submit = SubmitField('Add')

class ApplyForm(FlaskForm):
    grade = StringField('What grade did you get in this class?', validators=[DataRequired('Error, must enter a value'), AnyOf(values=['A', 'B', 'C'], message="Must be A, B, or C")])
    when_taken = StringField('When did you take this class?', validators=[DataRequired('Error, must enter a value'), Length(min = 6, max = 6, message='Must format in the style of A 2024 for example')])
    when_SA = StringField('When are you trying to SA this class?', validators=[DataRequired('Error, must enter a value'), Length(min = 6, max = 6, message='Must format in the style of A 2024 for example')])
    why = StringField('Why do you want to SA this class?', validators=[DataRequired('Error, must enter a value')])
    submit = SubmitField('Apply')

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')