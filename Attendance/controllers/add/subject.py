import psycopg2
from django.shortcuts import render

from Attendance.controllers.get.sql_connection import get_sql_connection


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    return render(
        request,
        'add_group.html')


def insert_into_subjects(schedule_id, subject):
    try:
        connection = get_sql_connection()
        cursor = connection.cursor()
        create_table_query = ''' INSERT INTO public.subjects(
                            schedule_id, subject)
                            VALUES (%s, %s);
                              '''

        record_tuple = (schedule_id, subject)
        cursor.execute(create_table_query, record_tuple)
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()


def add_subject(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    return render(
        request,
        'add_group.html')
