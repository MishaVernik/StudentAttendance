from datetime import datetime

import psycopg2

from Attendance.context.sql_connection import get_sql_connection


def if_student_on_the_lecture(student_id, date_original, date_plus20):
    try:
        connection = get_sql_connection()
        cursor = connection.cursor()
        postgre_sql_select_query = "SELECT * FROM public.attendance WHERE student_id=%s"

        cursor.execute(postgre_sql_select_query, (student_id,))
        #print("Selecting ifStudentOnTheLecture rows from mobile table using cursor.fetchall")
        mobile_records = cursor.fetchall()
        for row in mobile_records:
            student_id = row[0]
            date = datetime.strptime(row[1].split('.')[0], '%Y-%m-%d %H:%M:%S')
            if date_original <= date <= date_plus20:
                return True
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error ifStudentOnTheLecture while doing smth in PostgreSQL", error)
        student_or_teacher = 1
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        #print("PostgreSQL ifStudentOnTheLecture connection is closed")
    return False
