from datetime import datetime, timedelta

import psycopg2

from Attendance.controllers.get.sql_connection import get_sql_connection


def get_last_teachers_date():
    try:
        connection = get_sql_connection()
        cursor = connection.cursor()
        postgre_sql_select_query = "SELECT * from public.teachers_coordinates ORDER BY date DESC LIMIT 1;"
        cursor.execute(postgre_sql_select_query)
        print("Selecting ifStudentOnTheLecture rows from mobile table using cursor.fetchall")
        mobile_records = cursor.fetchall()
        date_plus20 = datetime.now()
        date_original = datetime.now()
        for row in mobile_records:
            date_original = datetime.strptime(row[3].split('.')[0], '%Y-%m-%d %H:%M:%S')

        return [date_original, date_original + timedelta(minutes=20)]
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error ifStudentOnTheLecture while doing smth in PostgreSQL", error)
        student_or_teacher = 1
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        print("PostgreSQL ifStudentOnTheLecture connection is closed")
    return ["", ""]
