from typing import Optional
from app import db
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from flask_login import UserMixin

class Course(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    coursenum : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(4), index=True)
    title : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(150))

    def __repr__(self):
        return '<Course {} - {} {}>'.format(self.id, self.coursenum, self.title)
    
    def get_coursenum(self):
        return self.coursenum
    
    def get_title(self):
        return self.title

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

class Instructor(User):
    __tablename__ = 'instructor'
    id : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(9), sqla.ForeignKey(User.id), primary_key=True)
    title : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'Instructor',
    }

    sections : sqlo.WriteOnlyMapped['Section'] = sqlo.relationship(back_populates = 'instructor')

    def __repr__(self):
        return '<Instructor {} - {} - {} {}>'.format(self.id, self.username, self.firstname, self.lastname)

class Student(User):
    __tablename__='student'
    major : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(50), nullable=True)
    GPA : sqlo.Mapped[float] = sqlo.mapped_column(sqla.Float(5), nullable=True)
    graduation_date : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(10), nullable=True)

    #Relationships
    
    __mapper_args__ = {
        'polymorphic_identity': 'Student'
    }

    def __repr__(self):
        return '<Student {} - {} - {} {}>'.format(self.id, self.username, self.firstname, self.lastname)

class Section(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    sectionnum : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(5))
    course_id : sqlo.Mapped[Course] = sqlo.mapped_column(sqla.ForeignKey(Course.id))

    instructor_id: sqlo.Mapped[str] = sqlo.mapped_column(sqla.ForeignKey('user.id'))
    instructor : sqlo.Mapped[Instructor] = sqlo.relationship(back_populates = 'sections')

    #Relationship
    # SA_Positions : sqlo.WriteOnlyMapped[SA_Position] = sqlo.relationship(back_populates = 'section')

    def __repr__(self):
        return '<Section - {} {}>'.format(self.get_course().title, self.sectionnum)
    
    def get_course(self):
        return db.session.scalars(sqla.select(Course).where(Course.id == self.course_id)).first()
    
class SA_Position(db.Model):
    section_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Section.id), primary_key=True)
    open_postions : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, default = 0)
    min_GPA : sqlo.Mapped[float] = sqlo.mapped_column(sqla.Float(5))
    min_Grade : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(1))

    #Relationship
    # section : sqlo.Mapped[Section] = sqlo.relationship(back_populates = 'SA_Positions')

@login.user_loader
def load_user(id):
    return db.session.get(User, id)
