from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
<<<<<<< HEAD
from django.shortcuts import render, redirect
=======
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, render_to_response
>>>>>>> 0afc7f21189e396d77670072b2508db1fc376e3c
from django.contrib import messages

from Attendance.Controllers.AddNewUsers import add_student, add_teacher
from Attendance.Controllers.CheckIfStudentOnTheLecture import if_student_on_the_lecture
from Attendance.Controllers.GetId import get_students_id, get_teachers_id
from Attendance.Controllers.GetSQLConnection import get_sql_connection
from Attendance.forms import SignUpStudentForm, SignUpTeacherForm
import psycopg2
from datetime import datetime, timedelta


<<<<<<< HEAD
=======
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

def getLastTeachersDate():
    try:
        connection = psycopg2.connect(user="cqwhbabxmaxxqd",
                                      password="a3063dc5aeec69b41564cd0f1e3c698e0ff9653385f3b87c0f113b70951eb5b3",
                                      host="ec2-54-235-92-244.compute-1.amazonaws.com",
                                      port="5432",
                                      database="d8d34m4nml4iij")

        cursor = connection.cursor()

        postgreSQL_select_Query = "SELECT * from public.teachers_coordinates ORDER BY date DESC LIMIT 1;"

        cursor.execute(postgreSQL_select_Query)
        print("Selecting ifStudentOnTheLecture rows from mobile table using cursor.fetchall")
        mobile_records = cursor.fetchall()
        datePlus20 = datetime.now()
        dateOriginal = datetime.now()
        for row in mobile_records:
            dateOriginal = datetime.strptime(row[0].split('.')[0], '%Y-%m-%d %H:%M:%S')

        return [dateOriginal, dateOriginal + timedelta(minutes=20)]
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error ifStudentOnTheLecture while doing smth in PostgreSQL", error)
        student_or_teacher = 1
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        print("PostgreSQL ifStudentOnTheLecture connection is closed")
    return ["",""]

def countNumberOsStudents():
    dates = getLastTeachersDate()
    try:
        connection = psycopg2.connect(user="cqwhbabxmaxxqd",
                                      password="a3063dc5aeec69b41564cd0f1e3c698e0ff9653385f3b87c0f113b70951eb5b3",
                                      host="ec2-54-235-92-244.compute-1.amazonaws.com",
                                      port="5432",
                                      database="d8d34m4nml4iij")

        cursor = connection.cursor()

        postgreSQL_select_Query = "SELECT COUNT(*) FROM public.attendance WHERE  date <= %s::date AND  date >= %s::date;"

        cursor.execute(postgreSQL_select_Query, (dates[1]), (dates[0]))
        print("Selecting ifStudentOnTheLecture rows from mobile table using cursor.fetchall")
        mobile_records = cursor.fetchall()
        number_of_students = 0
        for row in mobile_records:
            number_of_students = row[0]
        return number_of_students
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error ifStudentOnTheLecture while doing smth in PostgreSQL", error)
        student_or_teacher = 1
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        print("PostgreSQL ifStudentOnTheLecture connection is closed")
    return 0
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

>>>>>>> 0afc7f21189e396d77670072b2508db1fc376e3c
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

<<<<<<< HEAD
=======
@login_required
def homeTeacher(request):

    # number = countNumberOsStudents()
    # print("number : ", number)
    # stu = {
    #     "number": number
    # }
    return render(request, 'homeTeacher.html') #, stu)

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

>>>>>>> 0afc7f21189e396d77670072b2508db1fc376e3c

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
