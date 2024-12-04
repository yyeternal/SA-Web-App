from app import db, create_app
from config import Config
from app.main.models import Course, User, Student, SA_Position, Enrollment, Application
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo

from app.main.models import User, Instructor

app = create_app(Config)

@app.shell_context_processor
def make_shell_context():
    return {'sqla': sqla, 'sqlo': sqlo, 'db': db, 'Course': Course, 'User': User, 'Instructor': Instructor, 'Student': Student, 'SA_Position' : SA_Position, 'Enrollment' : Enrollment, 'Application' : Application}

def add_courses(*args, **kwargs):
    query = sqla.select(Course)
    if db.session.scalars(query).first() is None:
        courses = [('CS 3733', 'Software Engineering'), ('CS 1101', 'Intro to Program Design'), ('CS 3431', 'Database Systems'), ('CS 2223', 'Algorithms'), ('CS 2303', 'Systems Programming'), ('CS 3133', 'Foundations of CS'), ('CS 2011', 'Machine Org')]
        for n, c in courses: 
            course = Course(coursenum=n, title=c)
            db.session.add(course)
        db.session.commit()

@app.before_request
def initDB(*args, **kwargs):
    if app._got_first_request:
        db.create_all()
        add_courses(*args, **kwargs)
        
courses = [('CS 3733', 'Software Engineering'), ('CS 1101', 'Intro to Program Design'), ('CS 3431', 'Database Systems'), ('CS 2223', 'Algorithms'), ('CS 2303', 'Systems Programming'), ('CS 3133', 'Foundations of CS'), ('CS 2011', 'Machine Org')]

if __name__ == "__main__":
    app.run(debug=True)