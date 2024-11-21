from app import db
from app.instructor import instructor_blueprint as bp_instructor
from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.instructor.instructor_forms import CourseSectionForm, CreatePositionForm, EditInstructorProfileForm
from app.main.models import Section, SA_Position
from flask_login import login_required
import sqlalchemy as sqla

@bp_instructor.route('/course/create', methods=['GET', 'POST'])
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

@bp_instructor.route('/position/create', methods=['GET', 'POST'])
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

@bp_instructor.route('/instructor/edit', methods=['GET', 'POST'])
@login_required
def edit_instructor_profile():
    if current_user.user_type == 'Student':
        flash('You do not have access to this page')
        return redirect(url_for('main.index'))
    iform = EditInstructorProfileForm()
    if iform.validate_on_submit():
        current_user.firstname = iform.firstname.data
        current_user.lastname = iform.lastname.data
        current_user.phone_number = iform.phonenumber.data
        current_user.title = iform.title.data
        current_user.set_password(iform.password.data)
        db.session.commit()
        flash('Updated profile')
        return redirect(url_for('main.index'))
    return render_template('instructor_edit_profile.html', form = iform)