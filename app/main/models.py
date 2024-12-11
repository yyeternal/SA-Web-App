from typing import Optional
from app import db
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from flask_login import UserMixin
from datetime import datetime, timezone

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(9), primary_key=True)
    username : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(50))
    password_hash : sqlo.Mapped[Optional[str]] = sqlo.mapped_column(sqla.String(256))
    firstname : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(50))
    lastname : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(50))
    user_type : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(50))
    phone_number : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(15))

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': user_type
    }

    def __repr__(self):
        return '<User {} - {} - {} {}>'.format(self.id, self.username, self.firstname, self.lastname)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password=password)

    def check_password(self, password):
        return check_password_hash(pwhash=self.password_hash, password=password)
    
    def get_phone_number(self):
        return self.phone_number
    
    def get_username(self):
        return self.username

class Course(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    coursenum : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(7), index=True)
    title : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(150))

    # relationships
    positions : sqlo.WriteOnlyMapped['SA_Position'] = sqlo.relationship(back_populates= 'course')
    enrollments : sqlo.WriteOnlyMapped['Enrollment']  = sqlo.relationship(back_populates='course')

    def __repr__(self):
        return '<Course {} - {} {}>'.format(self.id, self.coursenum, self.title)
    
    def get_coursenum(self):
        return self.coursenum
    
    def get_title(self):
        return self.title
    
    def get_positions(self):
        return db.session.scalars(self.positions.select()).all()

class Instructor(User):
    __tablename__ = 'instructor'
    id : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(9), sqla.ForeignKey(User.id), primary_key=True)
    title : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'Instructor',
    }

    positions : sqlo.WriteOnlyMapped['SA_Position'] = sqlo.relationship(back_populates = 'instructor')
    applications : sqlo.WriteOnlyMapped['Application'] = sqlo.relationship(back_populates='instructor')

    def __repr__(self):
        return '<Instructor {} - {} - {} {}>'.format(self.id, self.username, self.firstname, self.lastname)
    
    def get_positions(self):
        return db.session.scalars(self.positions.select()).all()
    
    def get_applications(self):
        return db.session.scalars(self.applications.select()).all()
    
class SA_Position(db.Model):
    __tablename__ = 'sa_position'
    id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer(), primary_key=True)
    sectionnum : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(10))
    open_positions : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, default = 1)
    min_GPA : sqlo.Mapped[float] = sqlo.mapped_column(sqla.Float(5))
    min_Grade : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(1), nullable=True)
    timestamp : sqlo.Mapped[Optional[datetime]] = sqlo.mapped_column(default = lambda : datetime.now(timezone.utc))
    instructor_id : sqlo.Mapped[str] = sqlo.mapped_column(sqla.ForeignKey(Instructor.id))
    course_id : sqlo.Mapped['Course'] = sqlo.mapped_column(sqla.ForeignKey(Course.id))
    term : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(7))

    __table_args__ = (
        sqla.UniqueConstraint('sectionnum', 'course_id', 'term', name='unique_position'),
    )

    # relationships
    instructor : sqlo.Mapped['Instructor'] = sqlo.relationship(back_populates = 'positions')
    students : sqlo.WriteOnlyMapped['Student'] = sqlo.relationship(back_populates = 'position')
    applications : sqlo.WriteOnlyMapped['Application'] = sqlo.relationship(back_populates = 'position')
    course : sqlo.Mapped['Course'] = sqlo.relationship(back_populates = 'positions')

    def __repr__(self):
        return "".format()
    
    def get_SAs(self):
        return db.session.scalars(sqla.select(self.students.select())).all()

class Student(User):
    __tablename__='student'
    id : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(9), sqla.ForeignKey(User.id), primary_key=True)
    major : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(50))
    GPA : sqlo.Mapped[float] = sqlo.mapped_column(sqla.Float(5))
    graduation_date : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(10))
    isSA : sqlo.Mapped[bool] = sqlo.mapped_column(sqla.Boolean(), default=False)
    position_id: sqlo.Mapped[str] = sqlo.mapped_column(sqla.ForeignKey(SA_Position.id), nullable=True)

    # relationships
    enrollments : sqlo.WriteOnlyMapped['Enrollment'] = sqlo.relationship(back_populates='student')
    position : sqlo.Mapped['SA_Position'] = sqlo.relationship(back_populates = 'students')
    applications : sqlo.WriteOnlyMapped['Application'] = sqlo.relationship(back_populates = 'appStudent')

    __mapper_args__ = {
        'polymorphic_identity': 'Student'
    }

    def __repr__(self):
        return '<Student {} - {} - {} {}>'.format(self.id, self.username, self.firstname, self.lastname)
    
    def get_enrollments(self):
        return db.session.scalars(sqla.select(Enrollment).where(Enrollment.student_id == self.id)).all()
    
    def get_applications(self):
        return db.session.scalars(sqla.select(Application).where(Application.student_id == self.id)).all()

    def get_major(self):
        return self.major
    
    def get_GPA(self):
        return self.major
    
    def get_graduation_date(self):
        return self.major
    
class Enrollment(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    student_id : sqlo.Mapped[str] = sqlo.mapped_column(sqla.ForeignKey(Student.id))
    course_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Course.id))
    grade : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(1), nullable=True)
    wasSA : sqlo.Mapped[bool] = sqlo.mapped_column(sqla.Boolean())
    term : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(7))

    __table_args__ = (
        sqla.UniqueConstraint('student_id', 'course_id', 'wasSA', name='unique_enrollment'),
    )

    # relationships
    student : sqlo.Mapped['Student'] = sqlo.relationship(back_populates='enrollments')
    course : sqlo.Mapped['Course'] = sqlo.relationship(back_populates='enrollments')

    def get_course(self):
        return db.session.scalars(sqla.select(Course).where(Course.id == self.course_id)).first()

class Application(db.Model):
    __tablename__ = 'application'
    id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer(), primary_key=True)
    position_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey('sa_position.id'))
    grade_received : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(1))
    when_course_taken : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(50))
    when_SA : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(10))
    student_id: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(9), sqla.ForeignKey(Student.id))
    reasoning: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(300))
    status: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(20), default='Pending')
    instructor_id: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(9), sqla.ForeignKey(Instructor.id))

    # relationships
    appStudent : sqlo.Mapped['Student'] = sqlo.relationship(back_populates = 'applications')
    position : sqlo.Mapped['SA_Position'] = sqlo.relationship(back_populates = 'applications')
    instructor : sqlo.Mapped['Instructor'] = sqlo.relationship(back_populates = 'applications')

@login.user_loader
def load_user(id):
    return db.session.get(User, id)
