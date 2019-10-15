from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from Attendance.forms import SignUpStudentForm, SignUpTeacherForm
import psycopg2
from psycopg2 import Error
from datetime import datetime, timedelta


def ifStudentOnTheLecture(student_id, dateOriginal, datePlus20):
    try:
        connection = psycopg2.connect(user="cqwhbabxmaxxqd",
                                      password="a3063dc5aeec69b41564cd0f1e3c698e0ff9653385f3b87c0f113b70951eb5b3",
                                      host="ec2-54-235-92-244.compute-1.amazonaws.com",
                                      port="5432",
                                      database="d8d34m4nml4iij")

        cursor = connection.cursor()

        postgreSQL_select_Query = "SELECT * FROM public.attendance WHERE student_id=%s"

        cursor.execute(postgreSQL_select_Query, (student_id,))
        print("Selecting ifStudentOnTheLecture rows from mobile table using cursor.fetchall")
        mobile_records = cursor.fetchall()
        for row in mobile_records:
            student_id = row[0]
            date = datetime.strptime(row[1].split('.')[0], '%Y-%m-%d %H:%M:%S')

            print("123123123123")
            if (date >= dateOriginal and date <= datePlus20):
                return True
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error ifStudentOnTheLecture while doing smth in PostgreSQL", error)
        student_or_teacher = 1
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        print("PostgreSQL ifStudentOnTheLecture connection is closed")
    return False

def getStudentsId(user1):
    student_id = 0
    try:
        connection = psycopg2.connect(user="cqwhbabxmaxxqd",
                                      password="a3063dc5aeec69b41564cd0f1e3c698e0ff9653385f3b87c0f113b70951eb5b3",
                                      host="ec2-54-235-92-244.compute-1.amazonaws.com",
                                      port="5432",
                                      database="d8d34m4nml4iij")

        cursor = connection.cursor()

        postgreSQL_select_Query = "SELECT student_id, username FROM public.students WHERE username=%s"

        cursor.execute(postgreSQL_select_Query, (user1,))
        print("Selecting STUDENTS rows from mobile table using cursor.fetchall")
        mobile_records = cursor.fetchall()
        print(mobile_records)
        for row in mobile_records:
            student_id = row[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error STUDENTS while doing smth in PostgreSQL", error)
        student_or_teacher = 1
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        print("PostgreSQL STUDENTS connection is closed")

    return student_id
def getTeachersId(username):
    teachers_id = 0
    try:
        connection = psycopg2.connect(user="cqwhbabxmaxxqd",
                                      password="a3063dc5aeec69b41564cd0f1e3c698e0ff9653385f3b87c0f113b70951eb5b3",
                                      host="ec2-54-235-92-244.compute-1.amazonaws.com",
                                      port="5432",
                                      database="d8d34m4nml4iij")

        cursor = connection.cursor()

        postgreSQL_select_Query = "SELECT * FROM public.teachers WHERE username=%s"

        cursor.execute(postgreSQL_select_Query, (username,))
        print("Selecting TEACHERS rows from mobile table using cursor.fetchall")
        mobile_records = cursor.fetchall()
        for row in mobile_records:
            teachers_id = row[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error TEACHERS while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        print("PostgreSQL  TEACHERS connection is closed")
    return teachers_id

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
    print("HERE")

    return render(request, 'homeStudentLocation.html')

@login_required
def homeTeacher(request):
    return render(request, 'homeTeacher.html')

def calcLocationDiff(x1, y1, x2, y2):
    if (float(x1) - float(x2)) ** 2 + (float(y1)-float(y2))**2 < 100:
        return True
    return False

def getTeachersLocation(request):
    print("POST STARTS")
    # Get teachers Id
    teacher_id = 0
    print(request.POST['email'])
    try:
        connection = psycopg2.connect(user="cqwhbabxmaxxqd",
                                      password="a3063dc5aeec69b41564cd0f1e3c698e0ff9653385f3b87c0f113b70951eb5b3",
                                      host="ec2-54-235-92-244.compute-1.amazonaws.com",
                                      port="5432",
                                      database="d8d34m4nml4iij")

        cursor = connection.cursor()

        email = request.POST['email']
        postgreSQL_select_Query = "SELECT * FROM public.teachers WHERE public.teachers.email=%s"

        cursor.execute(postgreSQL_select_Query, (email,))
        print("Selecting rows from mobile table using cursor.fetchall")
        mobile_records = cursor.fetchall()

        print("Print each row and it's columns values")
        print(mobile_records)
        print('$'*50)
        for row in mobile_records:
            teacher_id = row[0]

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
    print("TEACHER ID " + str(teacher_id))
    try:
        connection = psycopg2.connect(user="cqwhbabxmaxxqd",
                                      password="a3063dc5aeec69b41564cd0f1e3c698e0ff9653385f3b87c0f113b70951eb5b3",
                                      host="ec2-54-235-92-244.compute-1.amazonaws.com",
                                      port="5432",
                                      database="d8d34m4nml4iij")

        cursor = connection.cursor()

        create_table_query = ''' INSERT INTO public.teachers_coordinates(
                           teachers_id, "date", latitude, longitude)
                            VALUES (%s, %s, %s, %s);
                              '''

        recordTuple = (teacher_id, datetime.now(), request.POST['latitude'], request.POST['longitude'])
        cursor.execute(create_table_query, recordTuple)
        connection.commit()

        print("Records successfully inserted in PostgreSQL")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")


    print(request.POST)
    print("POST ENDS")
    return render(request, 'homeTeacher.html')

def getStudentsLocation(request):
    print("POST STARTS")
    # Get teachers Id
    print(request.user)
    student_id = getStudentsId(str(request.user))
    student_arr = []

    print("STUDENT ID " + str(student_id))
    dateOriginal = datetime.now()
    datePlus20 = datetime.now()
    # Get last teachers visit
    latitude = 0
    longitude = 0
    try:
        connection = psycopg2.connect(user="cqwhbabxmaxxqd",
                                      password="a3063dc5aeec69b41564cd0f1e3c698e0ff9653385f3b87c0f113b70951eb5b3",
                                      host="ec2-54-235-92-244.compute-1.amazonaws.com",
                                      port="5432",
                                      database="d8d34m4nml4iij")

        cursor = connection.cursor()
        postgreSQL_select_Query = "SELECT teachers_id, date, latitude, longitude FROM public.teachers_coordinates ORDER BY date DESC LIMIT 1"

        cursor.execute(postgreSQL_select_Query)
        print("Selecting getStudentsLocation rows from mobile table using cursor.fetchall")
        mobile_records = cursor.fetchall()

        print("Print getStudentsLocation each row and it's columns values")
        print(mobile_records)
        print('$' * 50)

        for row in mobile_records:
            teacher_id = row[0]
            latitude = row[2]
            longitude = row[3]
            dateOriginal = datetime.strptime(row[1].split('.')[0], '%Y-%m-%d %H:%M:%S')
            datePlus20 = datetime.strptime(row[1].split('.')[0], '%Y-%m-%d %H:%M:%S')
        datePlus20 = datePlus20 + timedelta(minutes=20)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error getStudentsLocation while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        print("PostgreSQL getStudentsLocation connection is closed")
    # Check with date now
    # Check location difference between
    present = datetime.now()
    if present > datePlus20 or calcLocationDiff(request.POST['latitude'],request.POST['longitude'], latitude, longitude) == False or ifStudentOnTheLecture(student_id,dateOriginal,datePlus20):
        return render(request, 'home.html')
    try:
        connection = psycopg2.connect(user="cqwhbabxmaxxqd",
                                      password="a3063dc5aeec69b41564cd0f1e3c698e0ff9653385f3b87c0f113b70951eb5b3",
                                      host="ec2-54-235-92-244.compute-1.amazonaws.com",
                                      port="5432",
                                      database="d8d34m4nml4iij")

        cursor = connection.cursor()

        create_table_query = ''' INSERT INTO public.attendance(
                          student_id, date, latitude, longitude)
                            VALUES (%s, %s, %s, %s);
                              '''

        recordTuple = (student_id, datetime.now(), request.POST['latitude'], request.POST['longitude'],)
        cursor.execute(create_table_query, recordTuple)
        connection.commit()

        print("Records  attendance successfully inserted in PostgreSQL")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error attendance while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        print("PostgreSQL  attendance connection is closed")


    print(request.POST)
    print("POST ENDS")
    return render(request, 'home.html')

def add_student(first_name, second_name, group, email, github, username, password):
    try:
        connection = psycopg2.connect(user="cqwhbabxmaxxqd",
                                      password="a3063dc5aeec69b41564cd0f1e3c698e0ff9653385f3b87c0f113b70951eb5b3",
                                      host="ec2-54-235-92-244.compute-1.amazonaws.com",
                                      port="5432",
                                      database="d8d34m4nml4iij")

        cursor = connection.cursor()

        create_table_query = ''' INSERT INTO public.students(
                            first_name, second_name, email, "group", github, password, username)
                            VALUES (%s, %s, %s, %s, %s, %s, %s);
                              '''
        recordTuple = (first_name, second_name, email, group, github, password, username)
        cursor.execute(create_table_query, recordTuple)
        connection.commit()
        print("Records successfully inserted in PostgreSQL")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

def add_schedule(teacher_id, groups, name):
    try:
        connection = psycopg2.connect(user="cqwhbabxmaxxqd",
                                      password="a3063dc5aeec69b41564cd0f1e3c698e0ff9653385f3b87c0f113b70951eb5b3",
                                      host="ec2-54-235-92-244.compute-1.amazonaws.com",
                                      port="5432",
                                      database="d8d34m4nml4iij")

        cursor = connection.cursor()
        arr_groups = groups.split(',')
        print(arr_groups)
        for group in arr_groups:
            print(group)
            create_table_query = ''' INSERT INTO public.schedule(
                               teacher_id, "group", name)
                                VALUES (%s, %s, %s);
                                  '''
            recordTuple = (teacher_id, str(group), str(name))
            cursor.execute(create_table_query, recordTuple)
            connection.commit()

        print("Records schedule successfully inserted in PostgreSQL")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

def add_teacher(first_name, second_name, groups, email, faculty, username, password):
    try:
        connection = psycopg2.connect(user="cqwhbabxmaxxqd",
                                      password="a3063dc5aeec69b41564cd0f1e3c698e0ff9653385f3b87c0f113b70951eb5b3",
                                      host="ec2-54-235-92-244.compute-1.amazonaws.com",
                                      port="5432",
                                      database="d8d34m4nml4iij")

        cursor = connection.cursor()

        create_table_query = ''' INSERT INTO public.teachers(
                            first_name, second_name, email, faculty, password, username)
                            VALUES (%s, %s, %s, %s, %s, %s);
                              '''
        print('#'*40)
        recordTuple = (first_name, second_name, email,  faculty, password, username)
        cursor.execute(create_table_query, recordTuple)
        connection.commit()
        print('#' * 40)
        print("Records successfully inserted in PostgreSQL")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

    teacher_id = 0
    try:
        connection = psycopg2.connect(user="cqwhbabxmaxxqd",
                                      password="a3063dc5aeec69b41564cd0f1e3c698e0ff9653385f3b87c0f113b70951eb5b3",
                                      host="ec2-54-235-92-244.compute-1.amazonaws.com",
                                      port="5432",
                                      database="d8d34m4nml4iij")

        cursor = connection.cursor()

        postgreSQL_select_Query = "SELECT teacher_id FROM public.teachers ORDER BY teacher_id DESC LIMIT 1"

        cursor.execute(postgreSQL_select_Query)
        print("Selecting rows from mobile table using cursor.fetchall")
        mobile_records = cursor.fetchall()

        print("Print each row and it's columns values")
        print(mobile_records)
        print('$'*50)
        for row in mobile_records:
            teacher_id = row[0]

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
    print("TEACHRE ID " + str(teacher_id))
    add_schedule(teacher_id, groups, "SQL")
        
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
            #student_or_teacher = request.POST.get('')
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