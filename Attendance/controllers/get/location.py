from datetime import datetime, timedelta

import psycopg2
from django.shortcuts import render

from Attendance.controllers.check_if_student_on_the_lecture import if_student_on_the_lecture
from Attendance.controllers.get.id import get_students_id
from Attendance.controllers.calculate_distance import calculate_location_distance
from Attendance.context.sql_connection import get_sql_connection


def get_teachers_location(request):
    # get teachers Id
    teacher_id = 0
    #print(request.POST['email'])
    try:
        connection = get_sql_connection()
        cursor = connection.cursor()
        email = request.POST['email']
        postgre_sql_select_query = "SELECT * FROM public.teachers WHERE public.teachers.email=%s"
        cursor.execute(postgre_sql_select_query, (email,))
        mobile_records = cursor.fetchall()
        for row in mobile_records:
            teacher_id = row[0]

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
    try:

        connection = get_sql_connection()
        cursor = connection.cursor()
        create_table_query = ''' INSERT INTO public.teachers_coordinates(
                           teachers_id, "date", latitude, longitude, groups, subject, semester)
                            VALUES (%s, %s, %s, %s, %s, %s, %s);
                              '''
        #print(request.POST.getlist('group[]'))
        groups = ','.join(request.POST.getlist('groups[]'))
        #print('-' * 50)
        #print(groups)
        #print('-' * 50)
        record_tuple = (teacher_id, datetime.now(), request.POST['latitude'], request.POST['longitude'],
                        groups, request.POST.get('subject'), int(str(request.POST.get('semester')).split()[1]))
        cursor.execute(create_table_query, record_tuple)
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()

    return render(request, 'home_teacher.html')


def get_students_location(request):
    # get teachers Id
    #print(request.user)
    student_id = get_students_id(str(request.user))
    student_arr = []

    date_original = datetime.now()
    date_plus20 = datetime.now()
    # get last teachers visit
    latitude = 0
    longitude = 0
    try:
        connection = get_sql_connection()
        cursor = connection.cursor()
        postgre_sql_select_query = "SELECT teachers_id, date, latitude, longitude FROM public.teachers_coordinates " \
                                   "ORDER BY date DESC LIMIT 1 "
        cursor.execute(postgre_sql_select_query)
        mobile_records = cursor.fetchall()

        for row in mobile_records:
            teacher_id = row[0]
            latitude = row[2]
            longitude = row[3]
            date_original = datetime.strptime(row[1].split('.')[0], '%Y-%m-%d %H:%M:%S')
            date_plus20 = datetime.strptime(row[1].split('.')[0], '%Y-%m-%d %H:%M:%S')
        date_plus20 = date_plus20 + timedelta(minutes=20)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error getStudentsLocation while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        #print("PostgreSQL getStudentsLocation connection is closed")
    # Check with date now
    # Check location difference between
    present = datetime.now()
    if present > date_plus20 or calculate_location_distance(request.POST['latitude'], request.POST['longitude'],
                                                            latitude,
                                                            longitude) == False or if_student_on_the_lecture(student_id,
                                                                                                             date_original,
                                                                                                             date_plus20):
        return render(request, 'home.html')
    try:
        connection = get_sql_connection()
        cursor = connection.cursor()
        create_table_query = ''' INSERT INTO public.attendance(
                          student_id, date, latitude, longitude)
                            VALUES (%s, %s, %s, %s);
                              '''
        record_tuple = (student_id, datetime.now(), request.POST['latitude'], request.POST['longitude'],)
        cursor.execute(create_table_query, record_tuple)
        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error attendance while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
    return render(request, 'home.html')
