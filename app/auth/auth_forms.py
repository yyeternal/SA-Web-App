from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, FloatField 
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import  ValidationError, DataRequired, EqualTo, Email
from wtforms.widgets import ListWidget, CheckboxInput

from app.main.models import User, Instructor, Course
from app import db
import sqlalchemy as sqla

class LoginForm(FlaskForm):
    email = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember_me = BooleanField('Remember me?')
    submit = SubmitField('Sign In')

class StudentRegistrationForm(FlaskForm):
    username = StringField('Email', validators=[DataRequired('Error, must enter a value'), Email()])
    firstname = StringField('First Name', validators=[DataRequired('Error, must enter a value')])
    lastname = StringField('Last Name', validators=[DataRequired('Error, must enter a value')])
    WPI_id = StringField('WPI ID', validators=[DataRequired()])
    courses  = QuerySelectMultipleField('Courses Taken', 
                                        query_factory = lambda : db.session.scalars(sqla.select(Course)),
                                        get_label = lambda theCourse : theCourse.title,
                                        widget=ListWidget(prefix_label=False),
                                        option_widget = CheckboxInput())
    phonenumber = StringField('Phone Number', validators=[DataRequired()])
    major = StringField('Major', validators=[DataRequired()])
    gpa = FloatField('GPA', validators=[DataRequired()])
    graduation_date = StringField('Graduation Date', validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

   
    # def validate_username(self, username):
    #     query = sqla.select(Student).where(Student.username == username.data)
    #     user = db.session.scalars(query).first()
    #     if user is not None:
    #         raise ValidationError('Username already exists! Try another one')

    # def validate_email(self, email):
    #     query = sqla.select(Student).where(Student.email == email.data)
    #     user = db.session.scalars(query).first()
    #     if user is not None:
    #         raise ValidationError('Email already exists! Try another one')
    
    # def validate_WPIid(self, WPI_id):
    #     query = sqla.select(Stduent).where(Student.WPI_id == WPI_id.data)
    #     user = db.session.scalars(query).first()
    #     if user is not None:
    #         raise ValidationError('WPI ID already exists! Try another one')
        
    # validate_username(username)
    # validate_email(email)

class InstructorRegistrationForm(FlaskForm):
    username = StringField('Email', validators=[DataRequired('Error, must enter a value'), Email()])
    firstname = StringField('First Name', validators=[DataRequired('Error, must enter a value')])
    lastname = StringField('Last Name', validators=[DataRequired('Error, must enter a value')])
    WPI_id = StringField('WPI ID', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    phonenumber = StringField('Phone Number', validators=[DataRequired()])
    
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

   
    # def validate_username(self, username):
    #     query = sqla.select(Instructor).where(Instructor.username == username.data)
    #     user = db.session.scalars(query).first()
    #     if user is not None:
    #         raise ValidationError('Username already exists! Try another one')

    # def validate_email(self, email):
    #     query = sqla.select(Instructor).where(Instructor.username == email.data)
    #     user = db.session.scalars(query).first()
    #     if user is not None:
    #         raise ValidationError('Email already exists! Try another one')
    
    # def validate_WPIid(self, WPI_id):
    #     query = sqla.select(Instructor).where(Instructor.WPI_id == WPI_id.data)
    #     user = db.session.scalars(query).first()
    #     if user is not None:
    #         raise ValidationError('WPI ID already exists! Try another one')
        
    # validate_username(username)
    # validate_email(email)