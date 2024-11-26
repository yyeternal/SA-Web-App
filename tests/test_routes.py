"""
This file contains the functional tests for the main.
These tests use GETs and POSTs to different URLs to check for the proper behavior.
Resources:
    https://flask.palletsprojects.com/en/1.1.x/testing/ 
    https://www.patricksoftwareblog.com/testing-a-flask-application-using-pytest/ 
"""
import os
import pytest
from app import create_app, db
from app.main.models import User, Instructor, Student
from config import Config
import sqlalchemy as sqla


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = 'bad-bad-key'
    WTF_CSRF_ENABLED = False
    DEBUG = True
    TESTING = True


@pytest.fixture(scope='module')
def test_client():
    # create the flask application ; configure the app for tests
    flask_app = create_app(config_class=TestConfig)

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()
 
    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()
 
    yield  testing_client 
    # this is where the testing happens!
 
    ctx.pop()

def new_instructor(uname, ufirstname, ulastname, uuser_type, uphone_number, utitle, passwd):
    user = Instructor(username=uname, firstname=ufirstname, lastname=ulastname, user_type=uuser_type, phone_number=uphone_number, title = utitle)
    user.set_password(passwd)
    return user

def new_student(uname, ufirstname, ulastname, uuser_type, uphone_number, umajor, uGPA, ugraduation_date, uisSA, passwd):
    user = Student(username=uname, firstname=ufirstname, lastname=ulastname, user_type=uuser_type, phone_number=uphone_number, major=umajor, GPA=uGPA, graduation_date=ugraduation_date, isSA=uisSA)
    user.set_password(passwd)
    return user

# def init_tags():
#     # check if any tags are already defined in the database
#     count = db.session.scalar(db.select(db.func.count(Tag.id)))
#     print("**************", count)
#     # initialize the tags
#     if count == 0:
#         tags = ['funny','inspiring', 'true-story', 'heartwarming', 'friendship']
#         for t in tags:
#             db.session.add(Tag(name=t))
#         db.session.commit()
#     return None

@pytest.fixture
def init_database():
    # Create the database and the database table
    db.create_all()
    # initialize the tags
    #init_tags()
    #add a user    
    user1 = Instructor(username='profjohn@wpu.edu', firstname='john', lastname='instructor', user_type='Instructor', phone_number='1231231234', title = 'prof')
    user2 = Student(username='studjohn@wpu.edu', firstname='john', lastname='student', user_type='Instructor', phone_number='1231231234', major='CS', GPA=3.4, graduation_date='may2027', isSA=False)
    # Insert user data
    db.session.add(user1)
    db.session.add(user2)
    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()

def test_instructor_register_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/register' page is requested (GET)
    THEN check that the response is valid
    """
    # Create a test client using the Flask application configured for testing
    response = test_client.get('/instructor/register')
    assert response.status_code == 200
    assert b"Register" in response.data

def test_student_register_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/register' page is requested (GET)
    THEN check that the response is valid
    """
    # Create a test client using the Flask application configured for testing
    response = test_client.get('/student/register')
    assert response.status_code == 200
    assert b"Register" in response.data

def test_instructor_register(test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/register' form is submitted (POST)
    THEN check that the response is valid and the database is updated correctly
    """
    # Create a test client using the Flask application configured for testing
    response = test_client.post('/user/register', 
                          data=dict(username='profjohn@wpu.edu', firstname='john', lastname='instructor', user_type='Instructor', phone_number='1231231234', title = 'prof',password="bad-bad-password",password2="bad-bad-password"),
                          follow_redirects = True)
    assert response.status_code == 200
    
    s = db.session.scalars(sqla.select(User).where(User.username == 'profjohn@wpi.edu')).first()
    s_count = db.session.scalar(sqla.select(db.func.count()).where(User.username == 'profjohn@wpi.edu'))
    
    assert s.lastname == 'instructor'
    assert s_count == 1
    assert b"Sign In" in response.data   
    assert b"Please log in to access this page." in response.data

def test_student_register(test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/register' form is submitted (POST)
    THEN check that the response is valid and the database is updated correctly
    """
    # Create a test client using the Flask application configured for testing
    response = test_client.post('/user/register', 
                          data=dict(username='studjohn@wpi.edu',  firstname='john', lastname='student', user_type='Instructor', phone_number='1231231234', major='CS', GPA=3.4, graduation_date='may2027', isSA=False,password="bad-bad-password",password2="bad-bad-password"),
                          follow_redirects = True)
    assert response.status_code == 200
    
    s = db.session.scalars(sqla.select(User).where(User.username == 'studjohn@wpi.edu')).first()
    s_count = db.session.scalar(sqla.select(db.func.count()).where(User.username == 'studjohn@wpi.edu'))
    
    assert s.lastname == 'student'
    assert s_count == 1
    assert b"Sign In" in response.data   
    assert b"Please log in to access this page." in response.data

def test_invalidlogin(test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/login' form is submitted (POST) with wrong credentials
    THEN check that the response is valid and login is refused 
    """
    response = test_client.post('/user/login', 
                          data=dict(username='snow', password='12345',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data

# ------------------------------------
# Helper functions

def do_login(test_client, path , username, passwd):
    response = test_client.post(path, 
                          data=dict(username= username, password=passwd, remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    #Students should update this assertion condition according to their own page content
    assert b"Welcome to SA App!" in response.data  

def do_logout(test_client, path):
    response = test_client.get(path,                       
                          follow_redirects = True)
    assert response.status_code == 200
    # Assuming the application re-directs to login page after logout.
    #Students should update this assertion condition according to their own page content 
    assert b"Sign In" in response.data
    assert b"Please log in to access this page." in response.data    
# ------------------------------------

def test_login_logout(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/login' form is submitted (POST) with correct credentials
    THEN check that the response is valid and login is succesfull 
    """
    do_login(test_client, path = '/user/login', username = 'snow', passwd = '1234')

    do_logout(test_client, path = '/user/logout')



    
