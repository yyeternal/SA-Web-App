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
from app.main.models import User, Instructor, Student, Course, SA_Position, Enrollment, Application
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

def new_instructor(uname, ufirstname, ulastname, uuser_type, uphone_number, utitle, uid, passwd):
    user = Instructor(username=uname, firstname=ufirstname, lastname=ulastname, user_type=uuser_type, phone_number=uphone_number, id = uid, title = utitle)
    user.set_password(passwd)
    return user

def new_student(uname, ufirstname, ulastname, uuser_type, uphone_number, umajor, uGPA, ugraduation_date, uid, uisSA, passwd):
    user = Student(username=uname, firstname=ufirstname, lastname=ulastname, user_type=uuser_type, phone_number=uphone_number, major=umajor, GPA=uGPA, graduation_date=ugraduation_date, isSA=uisSA, id = uid)
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
    #user1 = Instructor(username='profjohn@wpu.edu', firstname='john', lastname='instructor', user_type='Instructor', phone_number='1231231234', title = 'prof', id = '333333333')
    user1 = new_instructor('profjohn@wpi.edu', 'john', 'instructor', 'Instructor', '1231231234', 'prof', '333333333', '123')
    user2 = new_student('studjohn@wpi.edu', 'john', 'student', 'Student', '1231231234', 'CS', 3.4, 'may2027', '444444444', False, '123')
    # Insert user data
    db.session.add(user1)
    db.session.add(user2)

    course1 = Course(coursenum = 'CS 3733',title='Software Engineering')
    course2 = Course(coursenum = 'CS 1101',title='Intro to CS')
    course3 = Course(coursenum = 'CS 1104',title='Intermediate to CS')
    db.session.add(course1)
    db.session.add(course2)
    db.session.add(course3)
    db.session.commit()

    position1 = SA_Position(sectionnum = 'section0', open_positions = 1, min_GPA = 3.0, min_Grade = 'A', instructor_id = user1.id, course_id = course2.id, term = 'A 2020')
    position2 = SA_Position(sectionnum = 'section7', open_positions = 1, min_GPA = 3.0, min_Grade = 'A', instructor_id = user1.id, course_id = course3.id, term = 'A 2020')
    db.session.add(position1)
    db.session.add(position2)

    enrollment1 = Enrollment(student_id = user2.id, course_id = course1.id, grade = 'A', wasSA = False, term = 'A 2020')
    db.session.add(enrollment1)

    db.session.commit()

    application1 = Application(position_id = position1.id, grade_received = 'A', when_course_taken = 'A 2020', when_SA = 'B 2020', student_id = user2.id, reasoning = 'want to ', status = 'Pending', instructor_id = user1.id)
    db.session.add(application1)


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

def test_instructor_register(request, test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/register' form is submitted (POST)
    THEN check that the response is valid and the database is updated correctly
    """
    custom_id = '777777777'
    custom_username = 'profmike@wpi.edu'
    # Create a test client using the Flask application configured for testing
    response = test_client.post('/instructor/register', 
                          data=dict(username = custom_username, 
                                    firstname='mike', 
                                    lastname='instructor', 
                                    WPI_id = custom_id, 
                                    phonenumber='2342342345', 
                                    title = 'prof', 
                                    password="bad-bad-password",
                                    password2="bad-bad-password"),
                          follow_redirects = True)
    assert response.status_code == 200
    
    user = db.session.scalars(sqla.select(User).where(User.id == custom_id)).first()
    assert user is not None
    assert user.id == custom_id

    users = db.session.scalars(sqla.select(User).where(User.id == custom_id)).all()
    assert user.lastname == 'instructor'
    assert len(users) == 1

    assert b"Congratulations, you are now a registered user!" in response.data   
    assert b"Sign In" in response.data

def test_student_register(request, test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/register' form is submitted (POST)
    THEN check that the response is valid and the database is updated correctly
    """
    custom_id = '888888888'
    custom_username = 'studmike@wpi.edu'
    # Create a test client using the Flask application configured for testing
    response = test_client.post('/student/register', 
                          data=dict(username=custom_username,  
                                    firstname='john', 
                                    lastname='student', 
                                    WPI_id=custom_id, 
                                    phonenumber='8908908900', 
                                    major='CS', 
                                    gpa=3.4, 
                                    graduation_date='May 2024', 
                                    password="bad-bad-password",
                                    password2="bad-bad-password"),
                          follow_redirects = True)
    assert response.status_code == 200
      
    user = db.session.scalars(sqla.select(User).where(User.id == custom_id)).first()
    assert user is not None
    assert user.id == custom_id

    users = db.session.scalars(sqla.select(User).where(User.id == custom_id)).all()
    assert len(users) == 1
    assert user.lastname == 'student'

    assert b"Congratulations, you are now a registered user!" in response.data   
    assert b"Sign In" in response.data

def test_invalidlogin(request, test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/login' form is submitted (POST) with wrong credentials
    THEN check that the response is valid and login is refused 
    """
    response = test_client.post('/user/login', 
                          data=dict(email='nouser', password='12345',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Sign In" in response.data
    assert b"Invalid username or password" in response.data

# ------------------------------------
# Helper functions

def do_login(test_client, path , uname, passwd):
    response = test_client.post(path, 
                          data=dict(email= uname, password=passwd, remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    #Students should update this assertion condition according to their own page content
    assert b"has succesfully logged in" in response.data  

def do_logout(test_client, path):
    response = test_client.get(path,                       
                          follow_redirects = True)
    assert response.status_code == 200
    # Assuming the application re-directs to login page after logout.
    #Students should update this assertion condition according to their own page content 
    assert b"Sign In" in response.data
# ------------------------------------

def test_instructor_login_logout(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/login' form is submitted (POST) with correct credentials
    THEN check that the response is valid and login is succesfull 
    """

    do_login(test_client, path = '/user/login', uname = 'profjohn@wpi.edu', passwd = '123')

    do_logout(test_client, path = '/user/logout')

def test_student_login_logout(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/login' form is submitted (POST) with correct credentials
    THEN check that the response is valid and login is succesfull 
    """

    do_login(test_client, path = '/user/login', uname = 'studjohn@wpi.edu', passwd = '123')

    do_logout(test_client, path = '/user/logout')



def test_create_SA_position(request, test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/register' form is submitted (POST)
    THEN check that the response is valid and the database is updated correctly
    """
    do_login(test_client, path = '/user/login', uname = 'profjohn@wpi.edu', passwd = '123')
    course = db.session.scalars(sqla.select(Course).where(Course.coursenum == 'CS 3733')).first()

    # Create a test client using the Flask application configured for testing
    response = test_client.post('/position/create', 
                          data=dict(course=course.id,  
                                    sectionnum='section1', 
                                    term='A 2024', 
                                    open_positions=2, 
                                    min_GPA=3.0, 
                                    min_grade='A'),
                          follow_redirects = True)
    assert response.status_code == 200
      
    position = db.session.scalars(sqla.select(SA_Position).where(SA_Position.course_id == course.id)).first()
    assert position is not None

    positions = db.session.scalars(sqla.select(SA_Position).where(SA_Position.course_id == course.id)).all()
    assert len(positions) == 1
    assert position.term == 'A 2024'
    assert position.open_positions == 2
    assert position.min_GPA == 3.0

    assert b"Added 2 new SA position(s) to course CS 3733-section1." in response.data   
    assert b"Student Assistant Positions" in response.data

    do_logout(test_client, path = '/user/logout')

def test_view_applications(request, test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/register' form is submitted (POST)
    THEN check that the response is valid and the database is updated correctly
    """
    do_login(test_client, path = '/user/login', uname = 'profjohn@wpi.edu', passwd = '123')
    #position = db.session.scalars(sqla.select(SA_Position).where(SA_Position.sectionnum == 'section0')).first()

    # Create a test client using the Flask application configured for testing
    response = test_client.post('/instructor/view_application/1?', 
                          follow_redirects = True)
    assert response.status_code == 200
    do_logout(test_client, path = '/user/logout')


def test_instructor_edit(request, test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/register' form is submitted (POST)
    THEN check that the response is valid and the database is updated correctly
    """
    do_login(test_client, path = '/user/login', uname = 'profjohn@wpi.edu', passwd = '123')
    # Create a test client using the Flask application configured for testing
    response = test_client.post('/instructor/edit', 
                          data=dict(firstname='mikal', 
                                    lastname='instructor', 
                                    title = 'instructor', 
                                    phonenumber='2342342345', 
                                    password="bad-bad-password",
                                    password2="bad-bad-password"),
                          follow_redirects = True)
    assert response.status_code == 200
    
    user = db.session.scalars(sqla.select(User).where(User.firstname == 'mikal')).first()
    assert user is not None

    users = db.session.scalars(sqla.select(User).where(User.firstname == 'mikal')).all()
    assert user.title == 'instructor'
    assert len(users) == 1

    assert b"Updated profile" in response.data   
    assert b"Student Assistant Positions for mikal" in response.data
    do_logout(test_client, path = '/user/logout')


def test_add_experience(request, test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/register' form is submitted (POST)
    THEN check that the response is valid and the database is updated correctly
    """
    course = db.session.scalars(sqla.select(Course).where(Course.coursenum == 'CS 3733')).first()
    do_login(test_client, path = '/user/login', uname = 'studjohn@wpi.edu', passwd = '123')
    # Create a test client using the Flask application configured for testing
    response = test_client.post('/student/course/add', 
                          data=dict(course=course.id, 
                                    grade='A', 
                                    wasSA = False, 
                                    term='A 2023'),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Course experience added" in response.data   
    do_logout(test_client, path = '/user/logout')

# def test_preexisting_enrollment(request, test_client,init_database):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/user/register' form is submitted (POST)
#     THEN check that the response is valid and the database is updated correctly
#     """
#     course = db.session.scalars(sqla.select(Course).where(Course.coursenum == 'CS 3733')).first()
#     # enrollment = db.session.scalars(sqla.select(Enrollment).where(Enrollment.term == 'A 2020')).first()
#     do_login(test_client, path = '/user/login', uname = 'studjohn@wpi.edu', passwd = '123')    #position = db.session.scalars(sqla.select(SA_Position).where(SA_Position.sectionnum == 'section0')).first()

#     # Create a test client using the Flask application configured for testing

#     response = test_client.post('/student/course/add', 
#                           data=dict(course=course.id, 
#                                     grade='A', 
#                                     wasSA = False, 
#                                     term='A 2020'),
#                           follow_redirects = True)
#     assert response.status_code == 200
#     assert b"already" in response.data   
#     do_logout(test_client, path = '/user/logout')


def test_view_my_applications(request, test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/register' form is submitted (POST)
    THEN check that the response is valid and the database is updated correctly
    """
    do_login(test_client, path = '/user/login', uname = 'studjohn@wpi.edu', passwd = '123')
    #position = db.session.scalars(sqla.select(SA_Position).where(SA_Position.sectionnum == 'section0')).first()

    # Create a test client using the Flask application configured for testing
    response = test_client.get('/applications/view', 
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"My Applications" in response.data   
    do_logout(test_client, path = '/user/logout')

def test_apply(request, test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/register' form is submitted (POST)
    THEN check that the response is valid and the database is updated correctly
    """
    do_login(test_client, path = '/user/login', uname = 'studjohn@wpi.edu', passwd = '123')
    position = db.session.scalars(sqla.select(SA_Position).where(SA_Position.sectionnum == 'section7')).first()

    # Create a test client using the Flask application configured for testing
    response = test_client.post('/student/'+ str(position.id) + '/apply', 
                          data=dict(grade='A', 
                                    when_taken='A 2024', 
                                    when_SA = 'B 2024', 
                                    why='want to'),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Application completed" in response.data   
    do_logout(test_client, path = '/user/logout')

def test_apply_exists(request, test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/user/register' form is submitted (POST)
    THEN check that the response is valid and the database is updated correctly
    """
    do_login(test_client, path = '/user/login', uname = 'studjohn@wpi.edu', passwd = '123')
    position = db.session.scalars(sqla.select(SA_Position).where(SA_Position.sectionnum == 'section0')).first()

    # Create a test client using the Flask application configured for testing
    response = test_client.post('/student/'+ str(position.id) + '/apply', 
                          data=dict(grade='A', 
                                    when_taken='A 2024', 
                                    when_SA = 'B 2024', 
                                    why='want to'),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"already" in response.data   
    do_logout(test_client, path = '/user/logout')
