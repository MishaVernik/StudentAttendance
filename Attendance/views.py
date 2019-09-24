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
        
        
def signUpTeacher(request):
    print(request)
    if request.method == 'POST':
        form = SignUpTeacherForm(request.POST)
        if form.is_valid():
            form.save()
            # student_or_teacher = request.POST.get('')
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
        form = SignUpTeacherForm()
    return render(request, 'signupTeacher.html', {'form': form})

def signupStudent(request):

    print(request)
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