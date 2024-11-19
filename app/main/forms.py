from flask_wtf import FlaskForm
from app import db

from app.main.models import User, Instructor
from wtforms import SelectField, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

class CourseSectionForm(FlaskForm):
    course = SelectField('Course', validators=[DataRequired()])
    section = StringField('Course Section', validators=[DataRequired()])
    term = StringField('Term', validators=[DataRequired()])
    submit = SubmitField('Add')

