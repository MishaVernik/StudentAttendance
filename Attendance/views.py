from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
import psycopg2
from psycopg2 import Error

@login_required
def home(request):
    return render(request, 'home.html')

def add_student(first_name, second_name, group, email, github, username, password):
    try:
        connection = psycopg2.connect(user="rsmoejupwkoewe",
                                      password="b884a8e0f70ca48fffe7f68007042862a0a19ed25223611f5db50005c14f82cf",
                                      host="ec2-54-221-212-126.compute-1.amazonaws.com",
                                      port="5432",
                                      database="dbqloi6h7obslf")

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
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def signup(request):
    print(request)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            student_or_teacher = request.POST.get('')
            first_name = form.cleaned_data.get("first_name")
            second_name = form.cleaned_data.get("second_name")
            group = form.cleaned_data.get("group")
            email = form.cleaned_data.get("email")
            github = form.cleaned_data.get("github")

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            # TODO: add user into PostgreSQL
            add_student(first_name, second_name, group, email, github, username, raw_password)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})