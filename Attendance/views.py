from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from Attendance.AddNewUsers import add_student, add_teacher
from Attendance.CheckIfStudentOnTheLecture import ifStudentOnTheLecture
from Attendance.GetId import getStudentsId, getTeachersId
from Attendance.forms import SignUpStudentForm, SignUpTeacherForm
import psycopg2
from datetime import datetime, timedelta

@login_required
def home(request):
    print("HOME")
    print(request.user)
    student_or_teacher = 0
    student_id = getStudentsId(str(request.user))
    teacher_id = getTeachersId(str(request.user))
    if student_id == 0:
        student_or_teacher = 1
    print(student_or_teacher)
    print(teacher_id)
    print(student_id)
    # var place
    testDate = datetime.now()
    datePlus20 = datetime.now()
    dateOriginal = datetime.now()
    latitude = ""
    longitude = ""
    teachers_id = 0
    try:
        connection = psycopg2.connect(user="cqwhbabxmaxxqd",
                                      password="a3063dc5aeec69b41564cd0f1e3c698e0ff9653385f3b87c0f113b70951eb5b3",
                                      host="ec2-54-235-92-244.compute-1.amazonaws.com",
                                      port="5432",
                                      database="d8d34m4nml4iij")

        cursor = connection.cursor()
        postgreSQL_select_Query = "SELECT teachers_id, date, latitude, longitude FROM public.teachers_coordinates ORDER BY date DESC LIMIT 1"

        cursor.execute(postgreSQL_select_Query)
        print("Selecting TEACHERS COORDINATES rows from mobile table using cursor.fetchall")
        mobile_records = cursor.fetchall()

        print("Print TEACHERS COORDINATES each row and it's columns values")
        print(mobile_records)
        print('134 ' + '$'*50)


        for row in mobile_records:
            teacher_id = row[0]
            latitude = row[2]
            longitude = row[3]
            dateOriginal = datetime.strptime(row[1].split('.')[0], '%Y-%m-%d %H:%M:%S')
            datePlus20 = datetime.strptime(row[1].split('.')[0], '%Y-%m-%d %H:%M:%S')

        datePlus20 = datePlus20 + timedelta(minutes=20)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error TEACHERS COORDINATES while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        print("PostgreSQL TEACHERS COORDINATES connection is closed")
    if student_or_teacher == 1:
        return render(request, 'homeTeacher.html')
    present = datetime.now()

    if (present > datePlus20 or ifStudentOnTheLecture(student_id, dateOriginal, datePlus20) or testDate + timedelta(minutes=20) == datePlus20):
        return render(request, 'home.html')
    return render(request, 'homeStudentLocation.html')

@login_required
def homeTeacher(request):

    # number = countNumberOsStudents()
    # print("number : ", number)
    # stu = {
    #     "number": number
    # }
    return render(request, 'homeTeacher.html') #, stu)

def signUpTeacher(request):
    print(request)
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

def signupStudent(request):

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