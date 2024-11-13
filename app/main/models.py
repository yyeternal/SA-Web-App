from app import db
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo


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
    