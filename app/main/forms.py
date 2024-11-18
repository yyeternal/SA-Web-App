from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired

class CourseSectionForm(FlaskForm):
    course = SelectField('Course', validators=[DataRequired()])
    section = StringField('Course Section', validators=[DataRequired()])
    term = StringField('Term', validators=[DataRequired()])
    submit = SubmitField('Add')