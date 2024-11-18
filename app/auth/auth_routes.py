from flask_wtf import FlaskForm
from app.main.models import User
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import  ValidationError, DataRequired, EqualTo, Email

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Error, must enter a value')])
    email = StringField('Email', validators= [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    validate_username(username)
    validate_email(email)
    def validate_username(self, username):
        query = sqla.select(User).where(User.username == username.data)
        user = db.session.scalars(query).first()
        if user is not None:
            raise ValidationError('Username already exists! Try another one')

    def validate_email(self, email):
        query = sqla.select(User).where(User.email == email.data)
        user = db.session.scalars(query).first()
        if user is not None:
            raise ValidationError('Email already exists! Try another one')