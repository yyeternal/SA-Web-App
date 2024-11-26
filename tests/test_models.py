import warnings
warnings.filterwarnings("ignore")

import unittest
from app import create_app, db
from app.main.models import User, Student, Instructor, SA_Position, Section, Course
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    
class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing_instructor(self):
        u = Instructor(username='john.prof@wpi.edu', firstname = 'john', lastname = 'instructor', user_type = 'Instructor', phone_number = '1231231234', title = 'prof')
        u.set_password('covid')
        self.assertFalse(u.check_password('flu'))
        self.assertTrue(u.check_password('covid'))

    def test_password_hashing_student(self):
        u = Instructor(username='john.stud@wpi.edu', firstname = 'john', lastname = 'student', user_type = 'Student', phone_number = '1231231234', major = 'cs', GPA = 3.4, graduation_date = 'may 2027', isSA = False)
        u.set_password('covid')
        self.assertFalse(u.check_password('flu'))
        self.assertTrue(u.check_password('covid'))

    def test_section_1(self):
        u1 = Instructor(username='john.prof@wpi.edu', firstname = 'john', lastname = 'instructor', user_type = 'Instructor', phone_number = '1231231234', title = 'prof')
        db.session.add(u1)
        db.session.commit()
        self.assertEqual(len(u1.get_sections()), 0)
        c1 = Course(coursenum = 3733, title = 'Software Engineering')
        db.session.add(c1)
        db.session.commit()
        s1 = Section(sectionnum='4', term='B', course_id=c1.id, instructor_id = u1.id)
        db.session.add(s1)
        db.session.commit()
        self.assertEqual(len(u1.get_sections()), 1)
        self.assertEqual(u1.get_sections()[0].sectionnum, '4')
        self.assertEqual(u1.get_sections()[0].term, 'B')

    def test_samecourse_differentsections(self):
        u1 = Instructor(username='john.prof@wpi.edu', firstname = 'john', lastname = 'instructor', user_type = 'Instructor', phone_number = '1231231234', title = 'prof')
        db.session.add(u1)
        db.session.commit()
        self.assertEqual(len(u1.get_sections()), 0)
        c1 = Course(coursenum = 3733, title = 'Software Engineering')
        db.session.add(c1)
        s1 = Section(sectionnum='4', term='B', course_id=c1.id, instructor_id = u1.id)
        db.session.add(s1)
        s2 = Section(sectionnum='5', term='A', course_id=c1.id, instructor_id = u1.id)
        db.session.add(s2)
        db.session.commit()
        # test the first section
        self.assertEqual(len(u1.get_sections()), 2)
        self.assertEqual(u1.get_sections()[0].sectionnum, '4')
        self.assertEqual(u1.get_sections()[0].term, 'B')
        # test the second section
        self.assertEqual(len(u1.get_user_posts()), 1)
        self.assertEqual(u1.get_sections()[0].sectionnum, '5')
        self.assertEqual(u1.get_sections()[0].term, 'A')



if __name__ == '__main__':
    unittest.main(verbosity=1)




    # def test_samecourse_differentsections(self):
    #     u1 = Instructor(username='john.prof@wpi.edu', firstname = 'john', lastname = 'instructor', user_type = 'Instructor', phone_number = '1231231234', title = 'prof')
    #     u2 = Instructor(username='smith.prof@wpi.edu', firstname = 'smith', lastname = 'instructor', user_type = 'Instructor', phone_number = '4564564567', title = 'prof')
    #     db.session.add(u1)
    #     db.session.add(u2)
    #     db.session.commit()
    #     self.assertEqual(len(u1.get_sections()), 0)
    #     self.assertEqual(len(u2.get_sections()), 0)
    #     c1 = Course(coursenum = 3733, title = 'Software Engineering')
    #     db.session.add(c1)
    #     s1 = Section(sectionnum='4', term='B', course_id=c1.id, instructor_id = u1.id)
    #     db.session.add(s1)
    #     s2 = Section(sectionnum='5', term='A', course_id=c1.id, instructor_id = u2.id)
    #     db.session.add(s2)
    #     db.session.commit()
    #     # test the posts by the first user
    #     self.assertEqual(len(u1.get_sections()), 2)
    #     self.assertEqual(u1.get_sections()[1].title, 'My post 2')
    #     self.assertEqual(u1.get_sections()[1].body, 'This is my second test post.')
    #     self.assertEqual(u1.get_user_posts()[1].happiness_level, 3)
    #     # test the posts by the second user
    #     self.assertEqual(len(u2.get_user_posts()), 1)
    #     self.assertEqual(u2.get_user_posts()[0].title, 'Another post')
    #     self.assertEqual(u2.get_user_posts()[0].body, 'This is a post by somebody else.')
    #     self.assertEqual(u2.get_user_posts()[0].happiness_level, 2)
    # c2 = Course(coursenum = 1001, title = 'CS intro')
    # db.session.add(c2)