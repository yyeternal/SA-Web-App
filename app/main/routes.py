from app.main import main_bluprint as bp_main
from flask import render_template
from app.main.forms import CourseSectionForm
from app.main.models import Section

@bp_main.route('/', methods=['GET'])
@bp_main.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

@bp_main.route('/course/create', methods=['GET'])
def create_course_section():
    cform = CourseSectionForm()
    if cform.validate_on_submit():
        section = Section(sectionnum=cform.section.data)