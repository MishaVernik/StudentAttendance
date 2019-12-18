import psycopg2

from Attendance.context.sql_connection import get_sql_connection


def get_students_id(user):
    student_id = 0
    try:
        connection = get_sql_connection()
        cursor = connection.cursor()
        postgre_sql_select_query = "SELECT student_id, username FROM public.students WHERE username=%s"
        cursor.execute(postgre_sql_select_query, (user,))
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
    return student_id


def get_teachers_id(username):
    teachers_id = 0
    try:
        connection = get_sql_connection()
        cursor = connection.cursor()
        postgre_sql_select_query = "SELECT * FROM public.teachers WHERE username=%s"
        cursor.execute(postgre_sql_select_query, (username,))
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
