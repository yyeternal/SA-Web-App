from flask_wtf import FlaskForm
from app import db
import sqlalchemy as sqla

from app.main.models import User, Instructor, Course
from wtforms import StringField, SubmitField, PasswordField, IntegerField, FloatField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from wtforms.widgets import ListWidget, CheckboxInput

class CourseSectionForm(FlaskForm):
    course = QuerySelectField('Course',
                         query_factory= lambda : db.session.scalars(sqla.select(Course)),
                         get_label= lambda c : 'CS{} - {}'.format(c.coursenum, c.title))
    section = StringField('Course Section', validators=[DataRequired()])
    term = StringField('Term', validators=[DataRequired()])
    submit = SubmitField('Add')

class CreatePositionForm(FlaskForm):
    section_id = QuerySelectField('Section',
                                 query_factory = 
                                 get_label = )
    open_positions = IntegerField('Number of Positions')
    min_GPA = FloatField('Minimum GPA of Student Assistant')
    min_grade = StringField('Minimum Grade of Student Assistant', validators=[Length(min = 0, max = 1)])
    submit = SubmitField('Create')
