from app import app, db
from app.main.models import Course, User, Section
from config import Config

import sqlalchemy as sqla
import sqlalchemy.orm as sqlo

app.app_context().push()

db.create_all()

c1 = Course(coursenum='CS3733', title="Software Engineering")
c2 = Course(coursenum='CS1101', title="Introduction to Program Design")

u1 = User(id='123456789', username='omreera@wpi.edu', firstname='Oliver', lastname='Reera', pnone_number='1234567890', user_type='Student')
u1.set_password('asdf')

s1 = Section(section_num='02', course_id=c1.id)