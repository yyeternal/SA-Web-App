from flask_wtf import FlaskForm
from flask_login import current_user
from app import db
import sqlalchemy as sqla

from app.main.models import User, Instructor, Course
from wtforms import StringField, SubmitField, PasswordField, IntegerField, FloatField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, NumberRange
from wtforms.widgets import ListWidget, CheckboxInput

class CreatePositionForm(FlaskForm):
    course = QuerySelectField('Course',
                         query_factory= lambda : db.session.scalars(sqla.select(Course)),
                         get_label= lambda c : '{} - {}'.format(c.coursenum, c.title))
    sectionnum = StringField('Section Number', validators=[DataRequired(), Length(min=1, max=10)])
    term = StringField('Term', validators=[DataRequired(), Length(min=1, max=6)])
    open_positions = IntegerField('Number of Positions', validators=[DataRequired(), NumberRange(min=1)])
    min_GPA = FloatField('Minimum GPA of Student Assistant', validators=[DataRequired(), NumberRange(min=0.01)])
    min_grade = StringField('Minimum Grade of Student Assistant', validators=[DataRequired(), Length(min = 1, max = 1)])
    submit = SubmitField('Create')


class EditInstructorProfileForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired('Error, must enter a value')])
    lastname = StringField('Last Name', validators=[DataRequired('Error, must enter a value')])
    title = StringField('Title', validators=[DataRequired()])
    phonenumber = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')