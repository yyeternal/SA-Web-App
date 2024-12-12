from app import db
from app.instructor import instructor_blueprint as bp_instructor
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.instructor.instructor_forms import CreatePositionForm, EditInstructorProfileForm
from app.main.models import SA_Position, Application, Instructor, Student
from flask_login import login_required
import sqlalchemy as sqla

@bp_instructor.route('/view_positions/view', methods=['GET'])
@login_required
def view_positions():
    if not current_user.user_type == 'Instructor':
        flash('You do not have access to this page')
        return redirect(url_for('main.index'))
    positions = SA_Position.query.filter_by(instructor_id=current_user.id).order_by(SA_Position.open_positions.desc()).all()

    return render_template('instructor.html', positions = positions)

@bp_instructor.route('/position/create', methods=['GET', 'POST'])
@login_required
def create_sa_position():
    if current_user.user_type == 'Student':
        flash('You do not have access to this page')
        return redirect(url_for('main.index'))
    pform = CreatePositionForm()
    if pform.validate_on_submit():
        new_SA_position = SA_Position(sectionnum = pform.sectionnum.data,
                                      open_positions = pform.open_positions.data,
                                      min_GPA = pform.min_GPA.data,
                                      min_Grade = pform.min_grade.data,
                                      instructor_id = current_user.id,
                                      course_id = pform.course.data.id,
                                      term = pform.term.data)
        db.session.add(new_SA_position)
        db.session.commit()
        flash('Added {} new SA position(s) to course {}-{}.'.format(pform.open_positions.data, pform.course.data.coursenum,pform.sectionnum.data))
        return redirect(url_for('main.index'))
    return render_template('create_position.html', form = pform)

@bp_instructor.route('/instructor/edit', methods=['GET', 'POST'])
@login_required
def edit_instructor_profile():
    if not current_user.user_type == 'Instructor':
        flash('You do not have access to this page')
        return redirect(url_for('main.index'))
    iform = EditInstructorProfileForm()
    if request.method == 'POST':
        if iform.validate_on_submit():
            current_user.firstname = iform.firstname.data
            current_user.lastname = iform.lastname.data
            current_user.phone_number = iform.phonenumber.data
            current_user.title = iform.title.data
            current_user.set_password(iform.password.data)
            db.session.commit()
            flash('Updated profile')
            return redirect(url_for('main.index'))
    elif request.method == 'GET':
        # populate form data from the DB
        iform.firstname.data = current_user.firstname
        iform.lastname.data = current_user.lastname
        iform.phonenumber.data = current_user.phone_number
        iform.title.data = current_user.title
    return render_template('instructor_edit_profile.html', form = iform)

@bp_instructor.route('/instructor/view_application/<position_id>', methods=['GET', 'POST'])
@login_required
def view_applications(position_id):
    if not current_user.user_type == 'Instructor':
        flash('You do not have access to this page')
        return redirect(url_for('main.index'))
    pending_applications = db.session.scalars(sqla.select(Application).where(Application.position_id == position_id).where(Application.instructor_id == current_user.id).where(Application.status == 'Pending')).all()
    approved_applications = db.session.scalars(sqla.select(Application).where(Application.position_id == position_id).where(Application.instructor_id == current_user.id).where(Application.status == 'Approved')).all()
    print(f"Number of applications found: {len(pending_applications)+len(approved_applications)}")
    apps = pending_applications + approved_applications
    return render_template('view_applications.html', title="Applications", applications=apps)

@bp_instructor.route('/instructor/approve_application/<application_id>', methods=['GET', 'POST'])
@login_required
def approve_applications(application_id):
    application = db.session.scalars(sqla.select(Application).where(Application.id == application_id)).first()
    if not current_user.user_type == 'Instructor' or not application.instructor_id == current_user.id:
        flash('You do not have access to this page')
        return redirect(url_for('main.index'))
    # application = Application.query.filter_by(position_id=int(position_id), status='Pending').first()
    position = application.position
    if (position.open_positions - 1) < 0:
        flash("Cannot approve, already accepted applicants for all available open positions")
        return redirect(url_for('main.index'))
    student = application.appStudent
    if student.isSA:
        flash("Cannot approve, student has already been accepted for a position")
        return redirect(url_for('main.index'))
    student.isSA = True
    position.open_positions -= 1
    application.status = 'Approved'
    db.session.commit()

    flash("Accepted students application!")
    return redirect(url_for('main.index'))

@bp_instructor.route('/instructor/reject_application/<application_id>', methods=['GET', 'POST'])
@login_required
def reject_applications(application_id):
    application = db.session.scalars(sqla.select(Application).where(Application.id == application_id)).first()
    if not current_user.user_type == 'Instructor' or not application.instructor_id == current_user.id:
        flash('You do not have access to this page')
        return redirect(url_for('main.index'))
    # position = SA_Position.query.get(position_id)
    # position = db.session.scalars(sqla.select(SA_Position).where(SA_Position.id == position_id)).first()
    # application = Application.query.filter_by(position_id=int(position_id), status='Pending').first()
    if application.status == 'REJECTED':
        flash("Already rejected application")
        return redirect(url_for('main.index'))
    elif application.status == 'Approved':
        flash('Cannot reject, already approved this application')
        return redirect(url_for('main.index'))
    position = application.position
    student = db.session.scalars(sqla.select(Student).where(Student.id == application.student_id)).first()
    if student.isSA and student.position == position:
        flash("Cannot reject, student has already been accepted for this position")
        return redirect(url_for('main.index'))
    application.status = 'REJECTED'
    db.session.commit()

    flash("REJECTED students application!")
    return redirect(url_for('main.index'))

@bp_instructor.route('/instructor/view_student/<student_id>', methods=['GET', 'POST'])
@login_required
def view_student(student_id):
    if not current_user.user_type == 'Instructor':
        flash('You do not have access to this page')
        return redirect(url_for('main.index'))
    student = Student.query.get(student_id)
    return render_template('display_profile.html', student=student)

@bp_instructor.route('/instructor/view_student_experience/<student_id>', methods=['GET', 'POST'])
@login_required
def view_student_experience(student_id):
    if not current_user.user_type == 'Instructor':
        flash('You do not have access to this page')
        return redirect(url_for('main.index'))
    student = Student.query.get(student_id)
    return render_template('student_experience.html', student=student)