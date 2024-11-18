from app import db
from app.main import main_blueprint as bp_main
from flask import render_template, flash, redirect, url_for
from app.main.forms import CourseSectionForm
from app.main.models import Section

@bp_main.route('/', methods=['GET'])
@bp_main.route('/index', methods=['GET'])
def index():
    return render_template('index.html', title='SA Recruitment Web App')

@bp_main.route('/course/create', methods=['GET'])
def create_course_section():
    cform = CourseSectionForm()
    if cform.validate_on_submit():
        new_section = Section(sectionnum=cform.section.data, course_id=cform.course.data.id)
        db.session.add(new_section)
        db.session.commit()
        flash('New course section created: {} {}'.format(new_section.get_course(), new_section.sectionnum))
        return redirect(url_for('main.index'))
    return render_template('create_course.html', title='SA Recruitment Web App', form=cform)