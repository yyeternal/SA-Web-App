import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from time import sleep
from app import db
from SAApp import app
from app.main.models import Course, User, Student, Instructor, SA_Position, Enrollment, Application
from config import Config

import sqlalchemy as sqla
import sqlalchemy.orm as sqlo


# User fixure - 1
@pytest.fixture
def inst1():
    return  {'username':'profjkohn@wpi.edu', 
             'firstname':'jjohn', 
             'lastname':'instructor', 
             'phone_number':'1231231234', 
             'id':'098763437', 
             'title':'prof', 
             'password':'123'}

@pytest.fixture
def editinst():
    return  {'title':'prof', 
             'firstname':'john', 
             'lastname':'instructor', 
             'phone_number':'1231231234', 
             'password':'123'}


# User fixure - 2
@pytest.fixture
def stud1():
    return  {'username':'studjkohn@wpi.edu', 
             'firstname':'jjohn', 
             'lastname':'student', 
             'id':'103048573', 
             'phonenumber':'4564564567', 
             'major':'CS', 
             'gpa':'3.5', 
             'graduation_date':'May 2025',
             'password':'123'}

 # Post fixure - 1
@pytest.fixture
def course1():
    return {'coursenum': 'CS 3733', 
            'title': 'Software Engineering'}

 # Post fixure - 2
@pytest.fixture
def pos1():
    return {'sectionnum': 'section0',
            'open_positions': '1', 
            'min_GPA': '3.0', 
            'min_Grade': 'A',  
            'term': 'A 2020' }

@pytest.fixture
def application1():
    return {'grade_received': 'A', 
            'when_course_taken': 'A 2020', 
            'when_SA': 'B 2020', 
            'reasoning': 'want to'}


"""
Download the chrome driver and make sure you have chromedriver executable in your PATH variable. 
To download the ChromeDriver to your system navigate to its download page. 
https://chromedriver.chromium.org/downloads  
"""

@pytest.fixture
def browser():
    CHROME_PATH = "C:/Users/alanw/Downloads/softeng/teamstack/tests"
    print(CHROME_PATH)

    service = Service(executable_path = CHROME_PATH + '\\chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(8)
    
    yield driver

    # For cleanup, quit the driver
    driver.quit()


def test_inst_register_form(browser,inst1):

    browser.get('http://127.0.0.1:5000/instructor/register')
    
    # Enable this to maximize the window
    # browser.maximize_window()
    browser.find_element(By.NAME, "username").send_keys(inst1['username'])
    ##############
    browser.find_element(By.NAME, "firstname").send_keys(inst1['firstname'])
    ##############
    browser.find_element(By.NAME, "lastname").send_keys(inst1['lastname'])
    ##############
    browser.find_element(By.NAME, "WPI_id").send_keys(inst1['id'])
    ##############
    browser.find_element(By.NAME, "title").send_keys(inst1['title'])
    ##############
    browser.find_element(By.NAME, "phonenumber").send_keys(inst1['phone_number'])
    ##############
    browser.find_element(By.NAME, "password").send_keys(inst1['password'])
    ##############
    browser.find_element(By.NAME, "password2").send_keys(inst1['password'])    
    ##############
    browser.find_element(By.NAME, "submit").click()
    ##############
    #verification
    content = browser.page_source
    # print(content)
    assert 'Congratulations, you are now a registered user!' in content

def test_inst_register_form_exist(browser,inst1):
    browser.get('http://127.0.0.1:5000/instructor/register')
    # Enable this to maximize the window
    # browser.maximize_window()
    browser.find_element(By.NAME, "username").send_keys(inst1['username'])
    ##############
    browser.find_element(By.NAME, "firstname").send_keys(inst1['firstname'])
    ##############
    browser.find_element(By.NAME, "lastname").send_keys(inst1['lastname'])
    ##############
    browser.find_element(By.NAME, "WPI_id").send_keys(inst1['id'])
    ##############
    browser.find_element(By.NAME, "title").send_keys(inst1['title'])
    ##############
    browser.find_element(By.NAME, "phonenumber").send_keys(inst1['phone_number'])
    ##############
    browser.find_element(By.NAME, "password").send_keys(inst1['password'])
    ##############
    browser.find_element(By.NAME, "password2").send_keys(inst1['password'])    
    ##############
    browser.find_element(By.NAME, "submit").click()
    ##############
    #verification
    sleep(5)
    content = browser.page_source
    # print(content)
    assert 'already' in content

def test_stud_register_form(browser,stud1):
    browser.get('http://127.0.0.1:5000/student/register')
    # Enable this to maximize the window
    # browser.maximize_window()
    browser.find_element(By.NAME, "username").send_keys(stud1['username'])
    ##############
    browser.find_element(By.NAME, "firstname").send_keys(stud1['firstname'])
    ##############
    browser.find_element(By.NAME, "lastname").send_keys(stud1['lastname'])
    ##############
    browser.find_element(By.NAME, "WPI_id").send_keys(stud1['id'])
    ##############
    browser.find_element(By.NAME, "phonenumber").send_keys(stud1['phonenumber'])
    ##############
    browser.find_element(By.NAME, "password").send_keys(stud1['password'])
    ##############
    browser.find_element(By.NAME, "password2").send_keys(stud1['password'])    
    ##############
    browser.find_element(By.NAME, "graduation_date").send_keys(stud1['graduation_date'])
    ##############
    browser.find_element(By.NAME, "major").send_keys(stud1['major'])
    ##############
    browser.find_element(By.NAME, "gpa").send_keys(stud1['gpa'])    
    ##############
    browser.find_element(By.NAME, "submit").click()
    ##############
    #verification
    content = browser.page_source
    # print(content)
    assert 'Congratulations, you are now a registered user!' in content

def test_login(browser,inst1):
    browser.get('http://127.0.0.1:5000/user/login')
    browser.find_element(By.NAME, "email").send_keys(inst1['username'])
    browser.find_element(By.NAME, "password").send_keys(inst1['password'])
    browser.find_element(By.NAME, "remember_me").click()
    browser.find_element(By.NAME, "submit").click()
    sleep(2)
    #verification
    content = browser.page_source
    assert 'succesfully' in content

def test_invalidlogin(browser,inst1):
    browser.get('http://127.0.0.1:5000/user/login')
    browser.find_element(By.NAME, "email").send_keys(inst1['username'])
    ##############
    browser.find_element(By.NAME, "password").send_keys('wrongpassword')
    ##############
    browser.find_element(By.NAME, "remember_me").click()
    ##############
    browser.find_element(By.NAME, "submit").click()
    ##############
    sleep(2)
    #verification
    content = browser.page_source
    assert 'Invalid username or password' in content
    assert 'Sign In' in content

def view_applications(browser,inst1):
    #first login
    browser.get('http://127.0.0.1:5000/user/login')
    browser.find_element(By.NAME, "email").send_keys(inst1['username'])
    browser.find_element(By.NAME, "password").send_keys(inst1['password'])
    browser.find_element(By.NAME, "remember_me").click()
    browser.find_element(By.NAME, "submit").click()

    browser.get('http://127.0.0.1:5000/instructor/view_application/1?')
    #verification
    content = browser.page_source
    assert 'Applications' in content

def test_instructor_edit(browser,inst1,editinst):
    #first login
    browser.get('http://127.0.0.1:5000/user/login')
    browser.find_element(By.NAME, "email").send_keys(inst1['username'])
    browser.find_element(By.NAME, "password").send_keys(inst1['password'])
    browser.find_element(By.NAME, "remember_me").click()
    browser.find_element(By.NAME, "submit").click()

    browser.get('http://127.0.0.1:5000/instructor/edit')
    browser.find_element(By.NAME, "title").send_keys(editinst['title'])
    ##############
    browser.find_element(By.NAME, "firstname").send_keys(editinst['firstname'])
    ##############
    browser.find_element(By.NAME, "lastname").send_keys(editinst['lastname'])
    ##############
    browser.find_element(By.NAME, "phonenumber").send_keys(editinst['phone_number'])
    ##############
    browser.find_element(By.NAME, "password").send_keys(editinst['password'])
    ##############
    browser.find_element(By.NAME, "password2").send_keys(editinst['password'])
    ##############
    browser.find_element(By.NAME, "submit").click()
    sleep(10)
    #verification
    content = browser.page_source
    assert "Updated profile" in content

def test_post_position(browser,inst1,pos1):
    #first login
    browser.get('http://127.0.0.1:5000/user/login')
    browser.find_element(By.NAME, "email").send_keys(inst1['username'])
    browser.find_element(By.NAME, "password").send_keys(inst1['password'])
    browser.find_element(By.NAME, "remember_me").click()
    browser.find_element(By.NAME, "submit").click()


    browser.get('http://127.0.0.1:5000/position/create')
    # #Select(browser.find_element(By.NAME, "course")).select_by_index(0)
    # Select(browser.find_element(By.NAME, 'course')).select_by_visible_text('CS 3733 - Software Engineering')
    ##############
    browser.find_element(By.NAME, "sectionnum").send_keys(pos1['sectionnum'])
    ##############
    browser.find_element(By.NAME, "term").send_keys(pos1['term'])
    ##############
    browser.find_element(By.NAME, "open_positions").send_keys(pos1['open_positions'])
    ##############
    browser.find_element(By.NAME, "min_GPA").send_keys(pos1['min_GPA'])
    ##############
    browser.find_element(By.NAME, "min_grade").send_keys(pos1['min_Grade'])
    ##############
    browser.find_element(By.NAME, "submit").click()
    ##############
    #verification
    sleep(2)
    content = browser.page_source
    assert 'Added' in content

    
if __name__ == "__main__":
    retcode = pytest.main(["-v"])
