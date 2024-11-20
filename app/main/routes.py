from app import db
from app.main import main_blueprint as bp_main
from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.main.forms import CourseSectionForm, CreatePositionForm
from app.main.models import Section, SA_Position
from flask_login import login_required
import sqlalchemy as sqla

@bp_main.route('/', methods=['GET'])
@bp_main.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('index.html', title='SA Recruitment Web App')

@bp_main.route('/course/create', methods=['GET', 'POST'])
@login_required
def create_course_section():
    if current_user.user_type == 'Student':
        flash('You do not have access to this page')
        return redirect(url_for('main.index'))
    cform = CourseSectionForm()
    if cform.validate_on_submit():
        new_section = Section(sectionnum=cform.section.data,
                              course_id=cform.course.data.id,
                              term=cform.term.data,
                              instructor=current_user,
                              instructor_id=current_user.id)
        db.session.add(new_section)
        db.session.commit()
        s = db.session.scalars(sqla.select(Section).where(Section.sectionnum == cform.section.data).where(Section.course_id == cform.course.data.id).where(Section.term == cform.term.data)).first()
        flash('New course section created: CS{}-{}'.format(s.get_course().coursenum,
                                                           s.sectionnum))
        return redirect(url_for('main.index'))
    return render_template('create_course.html', title='SA Recruitment Web App', form=cform)

@bp_main.route('/position/create', methods=['GET', 'POST'])
@login_required
def create_sa_position():
    if current_user.user_type == 'Student':
        flash('You do not have access to this page')
        return redirect(url_for('main.index'))
    pform = CreatePositionForm()
    if pform.validate_on_submit():
        new_SA_position = SA_Position(section_id = pform.section.data.id,
                                      open_positions = pform.open_positions.data,
                                      min_GPA = pform.min_GPA.data,
                                      min_Grade = pform.min_grade.data)
        db.session.add(new_SA_position)
        db.session.commit()
        if (pform.open_positions.data == 1):
            flash('New SA position added to course section.')
        else:
            flash('New SA positions added to course section.')
        return redirect(url_for('main.index'))
    return render_template('create_position.html', form = pform)
