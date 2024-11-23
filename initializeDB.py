from app import db
from SAApp import app
from app.main.models import Course, User, Section, Student, Instructor, SA_Position, Enrollment, Application
from config import Config

import sqlalchemy as sqla
import sqlalchemy.orm as sqlo

app.app_context().push()

db.create_all()

c1 = db.session.scalars(sqla.select(Course).where(Course.coursenum == 'CS 3733')).first()
c2 = db.session.scalars(sqla.select(Course).where(Course.coursenum == 'CS 1101')).first()
c3 = db.session.scalars(sqla.select(Course).where(Course.coursenum == 'CS 3431')).first()


u1 = Student(id='123456789', username='omreera@wpi.edu', firstname='Oliver', lastname='Reera', phone_number='1234567890', user_type='Student', major='CS', GPA=3.0, graduation_date='May 2024')
u1.set_password('asdf')
db.session.add(u1)

u2 = Instructor(id='987654321', username='sarslanay@wpi.edu', firstname='Sakire', lastname='Arslan Ay', phone_number='1234567890', user_type='Instructor', title='Prof')
u2.set_password('asdf')
db.session.add(u2)

u3 = Student(id='111111111', username='jdoe@wpi.edu', firstname='John', lastname='Doe', phone_number='1234567890', user_type='Student', major='RBE', GPA=2.8, graduation_date='May 2025')
u3.set_password('asdf')
db.session.add(u3)

u4 = Instructor(id='000000000', username='mahrens@wpi.edu', firstname='Matthew', lastname='Ahrens', phone_number='1234567890', user_type='Instructor', title='Prof')
u4.set_password('asdf')
db.session.add(u4)

db.session.commit()


s1 = Section(sectionnum='02', course_id=c1.id, instructor_id=u2.id, term='B 2024')
db.session.add(s1)

s2 = Section(sectionnum='01', course_id=c2.id, instructor_id=u4.id, term='C 2025')
db.session.add(s2)

s3 = Section(sectionnum='03', course_id=c3.id, instructor_id=u2.id, term='D 2025')
db.session.add(s3)

db.session.commit()


s1 = db.session.scalars(sqla.select(Section).where(Section.sectionnum=='02').where(Section.course_id==c1.id).where(Section.instructor_id==u2.id).where(Section.term=='B 2024')).first()
s2 = db.session.scalars(sqla.select(Section).where(Section.sectionnum=='01').where(Section.course_id==c2.id).where(Section.instructor_id==u4.id).where(Section.term=='C 2025')).first()
s3 = db.session.scalars(sqla.select(Section).where(Section.sectionnum=='03').where(Section.course_id==c3.id).where(Section.instructor_id==u2.id).where(Section.term=='D 2025')).first()


p1 = SA_Position(section_id=s1.id, min_GPA=3.0, min_Grade='B', open_positions=4)
db.session.add(p1)

p2 = SA_Position(section_id=s2.id, min_GPA=2.8, min_Grade='C', open_positions=3)
db.session.add(p2)

p3 = SA_Position(section_id=s3.id, min_GPA=3.4, min_Grade='A', open_positions=5)
db.session.add(p3)


e1 = Enrollment(student_id=u1.id, course_id=c1.id, grade='A', wasSA=False, term='B 2024')
db.session.add(e1)

e2 = Enrollment(student_id=u1.id, course_id=c2.id, wasSA=True, term='B 2024')
db.session.add(e2)

e2 = Enrollment(student_id=u3.id, course_id=c3.id, wasSA=True, term='A 2024')
db.session.add(e2)

db.session.commit()

a1 = Application(position_id=p1.id, grade_received='A', when_course_taken='A 2024', student_id=u1.id)
db.session.add(a1)

a2 = Application(position_id=p2.id, grade_received='A', when_course_taken='D 2024', student_id=u3.id)
db.session.add(a2)

a3 = Application(position_id=p3.id, grade_received='B', when_course_taken='C 2024', student_id=u1.id)
db.session.add(a3)

db.session.commit()

print('All values inserted')