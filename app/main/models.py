from app import db
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
from werkzeug.security import generate_password_hash, check_password_hash

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
    
class Section(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    sectionnum : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(5))
    course_id : sqlo.Mapped[Course] = sqlo.mapped_column(sqla.ForeignKey(Course.id))

    def __repr__(self):
        return '<Section - {} {}>'.format(self.get_course().title, self.sectionnum)
    
    def get_course(self):
        return db.session.scalars(sqla.select(Course).where(Course.id == self.course_id)).first()

class User(db.Model):
    id : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(9), primary_key=True)
    username : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(50))
    password_hash : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(256), nullable=True)
    firstname : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(50))
    lastname : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(50))
    user_type : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(50))
    phone_number : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(15))

    # __mapper_args__ = {
    #     'polymorphic_identity': 'User',
    #     'polymorphic_on': user_type
    # }

    def __repr__(self):
        return '<User {} - {} - {} {}>'.format(self.id, self.username, self.firstname, self.lastname)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password=password)

    def check_password(self, password):
        return check_password_hash(pwhash=self.password_hash, password=password)
