from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from Attendance.Controllers.AddNewUsers import add_student, add_teacher
from Attendance.Controllers.CheckIfStudentOnTheLecture import if_student_on_the_lecture
from Attendance.Controllers.GetId import get_students_id, get_teachers_id
from Attendance.Controllers.GetSQLConnection import get_sql_connection
from Attendance.forms import SignUpStudentForm, SignUpTeacherForm
import psycopg2
from datetime import datetime, timedelta


@login_required
def home(request):
    # var place
    student_id = get_students_id(str(request.user))
    teacher_id = get_teachers_id(str(request.user))
    student_or_teacher = 0

    if student_id == 0:
        student_or_teacher = 1

    test_date = datetime.now()
    date_plus20 = test_date
    date_original = test_date
    try:
        connection = get_sql_connection()
        cursor = connection.cursor()
        postgre_sql_select_query = "SELECT teachers_id, date, latitude, longitude FROM public.teachers_coordinates ORDER BY date DESC LIMIT 1"
        cursor.execute(postgre_sql_select_query)
        mobile_records = cursor.fetchall()
        for row in mobile_records:
            date_original = datetime.strptime(row[1].split('.')[0], '%Y-%m-%d %H:%M:%S')
            date_plus20 = datetime.strptime(row[1].split('.')[0], '%Y-%m-%d %H:%M:%S')

        date_plus20 = date_plus20 + timedelta(minutes=20)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error TEACHERS COORDINATES while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
    if student_or_teacher == 1:
        return render(request, 'homeTeacher.html')
    present = datetime.now()

    if (present > date_plus20) or if_student_on_the_lecture(student_id, date_original,
                                                            date_plus20) or test_date + timedelta(
            minutes=20) == date_plus20:
        return render(request, 'home.html')
    return render(request, 'homeStudentLocation.html')


@login_required
def home_teacher(request):
    return render(request, 'homeTeacher.html')


def sign_up_teacher(request):
    if request.method == 'POST':
        form = SignUpTeacherForm(request.POST)
        if form.is_valid():
            form.save()
            # student_or_teacher = request.POST.get('')
            first_name = form.cleaned_data.get('first_name')
            second_name = form.cleaned_data.get('last_name')
            groups = form.cleaned_data.get('groups')
            email = form.cleaned_data.get('email')
            faculty = form.cleaned_data.get('faculty')

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            messages.success(request, f'Account created for {username}')
            login(request, user)
            # TODO: add user into PostgreSQL
            add_teacher(first_name, second_name, groups, email, faculty, username, raw_password)
            return redirect('/accounts/profile/teacher/')
    else:
        form = SignUpTeacherForm()
    return render(request, 'signupTeacher.html', {'form': form})


def signup_student(request):
    if request.method == 'POST':
        form = SignUpStudentForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            second_name = form.cleaned_data.get('last_name')
            group = form.cleaned_data.get('group')
            email = form.cleaned_data.get('email')
            github = form.cleaned_data.get('github')

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            messages.success(request, f'Account created for {username}')
            login(request, user)

            add_student(first_name, second_name, group, email, github, username, raw_password)
            return redirect('home')
    else:
        form = SignUpStudentForm()
    return render(request, 'signupStudent.html', {'form': form})