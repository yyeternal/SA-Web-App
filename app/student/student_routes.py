from app import db
from app.student import student_blueprint as bp_student
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.main.models import SA_Position, Enrollment, Application, Student
from app.student.student_forms import EditStudentProfileForm, AddCourseForm, ApplyForm, EmptyForm
from flask_login import login_required
import sqlalchemy as sqla
import numpy as np
from pymcdm.methods import TOPSIS
from pymcdm.helpers import rrankdata

@bp_student.route('/positions/view', methods=['GET'])
@login_required
def view_positions():
    if not current_user.user_type == 'Student':
        flash('You do not have access to this page')
        return redirect(url_for('main.index'))
    positions = db.session.scalars(sqla.select(SA_Position).where(SA_Position.open_positions > 0).order_by(SA_Position.open_positions.desc())).all()
    return render_template('student.html', positions=positions)

@bp_student.route('/positions/view/recommended', methods=['GET'])
@login_required
def view_recommended_positions():
    if not current_user.user_type == 'Student':
        flash('You do not have access to this page')
        return redirect(url_for('main.index'))
    positions = db.session.scalars(sqla.select(SA_Position).where(SA_Position.open_positions > 0)).all()
    # TODO: develop algorithm to filter/sort positions by recommendation rank
    positions = list(positions)
    dmat = []
    ranked_positions = []
    grades = {"A": 3, "B": 2, "C": 1}
    # filter out positions that have qualifications that are too high, e.g. GPA or grade is not high enough
    for p in positions:
        class_taken = db.session.scalars(sqla.select(Enrollment).where(Enrollment.student_id == current_user.id).where(Enrollment.course_id == p.course_id).where(Enrollment.wasSA == False)).first()
        class_sa = db.session.scalars(sqla.select(Enrollment).where(Enrollment.student_id == current_user.id).where(Enrollment.course_id == p.course_id).where(Enrollment.wasSA)).first()
        if class_taken is not None and grades[p.min_Grade] > grades[class_taken.grade]: # remove if min grade required is "less than" (comes before in alphabet) grade received
            continue
        if p.min_GPA > current_user.GPA:
            continue
        ranked_positions.append(p)
        row = [int(class_sa is not None), (current_user.GPA - p.min_GPA) / 4, (ord(class_taken.grade) - ord(p.min_Grade)) if class_taken is not None else 0]
        dmat.append(row)
    if not len(ranked_positions) == 0 and not len(ranked_positions) == 1:
        # sort based on if student has SA'd for the class before, difference btwn GPA and min_GPA, difference btwn grade and min_Grade
        data = np.array(dmat)
        weights = np.array([0.4, 0.3, 0.3])
        types = np.array([1, -1, 1])

        topsis = TOPSIS()
        
        pref = topsis(data, weights=weights, types=types)
        ranking = rrankdata(pref)
        ranked_positions = [val for (_, val) in sorted(zip(ranking, ranked_positions), key=lambda x: x[0])]

        return render_template('student.html', positions=ranked_positions, rec=True)
    else:
        return render_template('student.html', positions=ranked_positions, rec=True)

@bp_student.route('/applications/view', methods=['GET'])
@login_required
def view_applications():
    if not current_user.user_type == 'Student':
        flash('You do not have access to this page')
        return redirect(url_for('main.index'))
    applications = db.session.scalars(sqla.select(Application).where(Application.student_id == current_user.id).where(Application.status != 'Withdrawn')).all()
    return render_template('student_applications.html', applications = applications)

@bp_student.route('/positions/<position_id>/view', methods=['GET'])
@login_required
def view_selected_position(position_id):
    if not current_user.user_type == 'Student':
        flash('You do not have access to this page')
        return redirect(url_for('main.index'))
    sa_position = db.session.scalars(sqla.select(SA_Position).where(SA_Position.id == int(position_id))).first()
    term = sa_position.term
    min_GPA = sa_position.min_GPA
    min_Grade = sa_position.min_Grade
    return render_template('student.html', sa_position = sa_position, term = term, min_GPA = min_GPA, min_Grade = min_Grade)

@bp_student.route('/student/edit', methods=['GET', 'POST'])
@login_required
def edit_student_profile():
    if not current_user.user_type == 'Student':
        flash('You do not have access to this page')
        return redirect(url_for('main.index'))
    sform = EditStudentProfileForm()
    if request.method == 'POST':
        if sform.validate_on_submit():
            current_user.firstname = sform.firstname.data
            current_user.lastname = sform.lastname.data
            current_user.phone_number = sform.phonenumber.data
            current_user.major = sform.major.data
            current_user.GPA = sform.gpa.data
            current_user.graduation_date = sform.graduation_date.data
            current_user.set_password(sform.password.data)
            db.session.commit()
            flash('Updated profile')
            return redirect(url_for('main.index'))
    elif request.method == 'GET':
        # populate form data from the DB
        sform.firstname.data = current_user.firstname
        sform.lastname.data = current_user.lastname
        sform.phonenumber.data = current_user.phone_number
        sform.major.data = current_user.major
        sform.gpa.data = current_user.GPA
        sform.graduation_date.data = current_user.graduation_date
    return render_template('student_edit_profile.html', form = sform)

@bp_student.route('/student/course/add', methods=['GET', 'POST'])
@login_required
def student_add_course():
    if not current_user.user_type == 'Student':
        flash('You do not have access to this page')
        return redirect(url_for('main.index'))
    aform = AddCourseForm()
    if aform.validate_on_submit():
        e = db.session.scalars(sqla.select(Enrollment).where(Enrollment.student_id == current_user.id).where(Enrollment.course_id == aform.course.data.id).where(Enrollment.wasSA == aform.wasSA.data)).first()
        if e is None:
            new_enrollment = Enrollment(student_id=current_user.id, course_id=aform.course.data.id, grade=aform.grade.data.upper(), wasSA=aform.wasSA.data, term=aform.term.data)
            db.session.add(new_enrollment)
            db.session.commit()
            flash('Course experience added')
            return redirect(url_for('main.index'))
        flash('Enrollment already exists')
    return render_template('add_experience.html', form=aform)

@bp_student.route('/student/<position_id>/apply', methods=['GET', 'POST'])
@login_required
def student_apply_position(position_id):
    if not current_user.user_type == 'Student':
        flash('You do not have access to this page')
        return redirect(url_for('main.index'))
    already_applied = db.session.scalars(sqla.Select(Application).where(Application.student_id == current_user.id, Application.position_id==int(position_id))).first()
    if already_applied is not None:
        flash('You already applied for this position!')
        return redirect(url_for('main.index'))
    if current_user.isSA:
        flash('You have already been accepted to a position!')
        return redirect(url_for('main.index'))
    position = db.session.scalars(sqla.select(SA_Position).where(SA_Position.id == int(position_id))).first()
    student = db.session.scalars(sqla.select(Student).where(Student.id==current_user.id)).first()
    class_taken = db.session.scalars(sqla.select(Enrollment).where(Enrollment.student_id == student.id, Enrollment.course_id == position.course_id)).first()
    apform = ApplyForm()
    if class_taken is not None:
        apform.grade.data = class_taken.grade
        apform.when_taken.data = class_taken.term
    if apform.validate_on_submit():
        instructor_id = position.instructor_id
        application = Application(position_id = position_id,
                                    grade_received = apform.grade.data,
                                    when_course_taken = apform.when_taken.data,
                                    when_SA = apform.when_SA.data,
                                    reasoning = apform.why.data, 
                                    student_id = current_user.id,
                                    instructor_id = instructor_id)
        db.session.add(application)
        db.session.commit()
        flash('Application completed!')
        return redirect(url_for('main.index'))
    return render_template('apply.html', form=apform, position=position, class_taken=class_taken)
    
@bp_student.route('/student/<application_id>/withdraw', methods=['POST', 'GET'])
@login_required
def withdraw(application_id):
    if not current_user.user_type == 'Student':
        flash('You do not have access to this page')
        return redirect(url_for('main.index'))
    theapplication = db.session.get(Application, application_id)
    if theapplication is None:
        flash("Idk bro")
        return redirect(url_for('main.index'))
    theapplication.status = 'Withdrawn'
    db.session.add(theapplication)
    db.session.commit()
    flash('You succesfully withdrew this application!')
    applications = db.session.scalars(sqla.select(Application).where(Application.student_id == current_user.id)).all()
    return render_template('student_applications.html', applications = applications)

@bp_student.route('/<student_id>/profile', methods=['GET'])
@login_required
def display_profile(student_id):
    empty_form = EmptyForm()
    return render_template('display_profile.html', title = 'Display Profile', student = db.session.scalars(sqla.Select(Student).where(Student.id == student_id)), form = empty_form)

@bp_student.route('/experience/view', methods=['GET'])
@login_required
def view_experience():
    if not current_user.user_type == 'Student':
        flash('You do not have access to this page')
        return redirect(url_for('main.index'))
    enrollments = current_user.get_enrollments()
    return render_template('_student_experience.html', enrollments = enrollments)

@bp_student.route('/student/<experience_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_exp(experience_id):
    if not current_user.user_type == 'Student':
        flash('You do not have access to this page')
        return redirect(url_for('main.index'))
    the_exp = db.session.get(Enrollment, experience_id)
    if the_exp is None:
        flash("Idk bro")
        return redirect(url_for('main.index'))
    db.session.delete(the_exp)
    db.session.commit()
    flash('You succesfully deleted that previous experience!')
    # enrollments = current_user.get_enrollments()
    return redirect(url_for("student.view_experience"))
