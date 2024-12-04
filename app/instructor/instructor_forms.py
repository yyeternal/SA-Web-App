from flask_wtf import FlaskForm
from flask_login import current_user
from app import db
import sqlalchemy as sqla

from app.main.models import User, Instructor, Course, Section
from wtforms import StringField, SubmitField, PasswordField, IntegerField, FloatField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, NumberRange
from wtforms.widgets import ListWidget, CheckboxInput

class CourseSectionForm(FlaskForm):
    course = QuerySelectField('Course',
                         query_factory= lambda : db.session.scalars(sqla.select(Course)),
                         get_label= lambda c : '{} - {}'.format(c.coursenum, c.title))
    section = StringField('Course Section', validators=[DataRequired()])
    term = StringField('Term', validators=[DataRequired()])
    submit = SubmitField('Add')


class CreatePositionForm(FlaskForm):
    section = QuerySelectField('Section',
                                 query_factory = lambda : db.session.scalars(sqla.select(Section).where(Section.instructor_id == current_user.id)),
                                 get_label = lambda s : '{} {}'.format(db.session.scalars(sqla.select(Course).where(Course.id == s.course_id)).first().coursenum, s.sectionnum))
    open_positions = IntegerField('Number of Positions', validators=[DataRequired()])
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