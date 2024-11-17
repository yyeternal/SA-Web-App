from app import db
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo


class Course(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    coursenum : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(4), index=True)
    major : 
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

class User(db.Model):
    id : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(9))
    username : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(50))
    password_hash : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(100))
    firstname : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(50))
    lastname : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(50))
    user_type : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(50))
    phone_number : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(15))

    __mapper_args__ = {
        'polymorphic_identity': 'User',
        'polymorphic_on': user_type
    }

    def __repr__(self):
        return '<User {} - {} - {} {}>'.format(self.id, self.username, self.firstname, self.lastname)
