import psycopg2

from Attendance.context.sql_connection import get_sql_connection


def students_group(user):
    _group = 0
    try:
        connection = get_sql_connection()
        cursor = connection.cursor()
        postgre_sql_select_query = 'SELECT "group", username FROM public.students WHERE username=%s'
        cursor.execute(postgre_sql_select_query, (user,))
        mobile_records = cursor.fetchall()
        #print(mobile_records)
        for row in mobile_records:
            _group = row[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error STUDENTS while doing smth in PostgreSQL", error)
        student_or_teacher = 1
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
    return _group