from app import db
from app.main import main_blueprint as bp_main
from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.main.forms import CourseSectionForm
from app.main.models import Section
from flask_login import login_required

@bp_main.route('/', methods=['GET'])
@bp_main.route('/index', methods=['GET'])
@login_required
@login_required
def index():
    return render_template('index.html', title='SA Recruitment Web App')

@bp_main.route('/course/create', methods=['GET'])
@login_required
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
                              instructor=current_user,
                              instructor_id=current_user.id)
        db.session.add(new_section)
        db.session.commit()
        flash('New course section created: CS{}-{}'.format(new_section.get_course().coursenum,
                                                           new_section.sectionnum))
        return redirect(url_for('main.index'))
    return render_template('create_course.html', title='SA Recruitment Web App', form=cform)

@bp_main.route('/position/create', methods=['GET', 'POST'])
@login_required
def create_sa_position():
    if current_user.user_type == 'Student':
        flash('You do not have access to this page')
        return redirect(url_for('main.index'))
    return render_template('create_position.html')