import psycopg2
from django.shortcuts import render

from Attendance.controllers.add.subject import insert_into_subjects
from Attendance.controllers.get.id import get_teachers_id
from Attendance.controllers.get.sql_connection import get_sql_connection


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """

    return render(
        request,
        'add_group.html')


def get_id(teacher_id, group, semester):
    try:
        connection = get_sql_connection()
        cursor = connection.cursor()
        postgre_sql_select_query = 'SELECT id from public.schedule WHERE teacher_id=%s AND "group"=%s AND semester=%s;'
        cursor.execute(postgre_sql_select_query, (teacher_id, group, semester), )
        mobile_records = cursor.fetchall()

        for row in mobile_records:
            return row[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error ifStudentOnTheLecture while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        print("PostgreSQL ifStudentOnTheLecture connection is closed")
    return -1


def add_group(request):
    """

    """
    print(request.user)
    semester = request.POST.get('semester').split()
    subject = request.POST.get('subject')
    teacher_id = get_teachers_id(str(request.user))

    groups = request.POST.get('group').split(',')
    for group in groups:
        try:
            connection = get_sql_connection()
            cursor = connection.cursor()
            create_table_query = ''' INSERT INTO public.schedule(
                                teacher_id, "group", semester)
                                VALUES (%s, %s, %s);
                                  '''

            record_tuple = (teacher_id, group, semester[1])
            cursor.execute(create_table_query, record_tuple)
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while doing smth in PostgreSQL", error)
        finally:
            # closing database connection.
            cursor.close()
            connection.close()

        if len(subject) > 0:
            schedule_id = get_id(teacher_id=teacher_id, group=group, semester=semester[1])
            if schedule_id == -1:
                pass
            else:
                insert_into_subjects(schedule_id, subject)
    return render(
        request,
        'home.html')
