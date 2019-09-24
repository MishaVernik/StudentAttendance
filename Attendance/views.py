from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages

from Attendance.forms import SignUpStudentForm, SignUpTeacherForm
import psycopg2
from psycopg2 import Error

@login_required
def home(request):
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
            return redirect('home')
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
            # TODO: add user into PostgreSQL
            add_student(first_name, second_name, group, email, github, username, raw_password)
            return redirect('home')
    else:
        form = SignUpStudentForm()
    return render(request, 'signupStudent.html', {'form': form})