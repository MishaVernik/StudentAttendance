from datetime import datetime, timedelta

import psycopg2

from Attendance.controllers.get.sql_connection import get_sql_connection


# Gets all dates by teachers_id & subject & semester
def all_dates(teacher_id, subject, semester, groups):
    global connection, cursor
    dates = []
    try:
        connection = get_sql_connection()
        cursor = connection.cursor()
        postgre_sql_select_query = 'SELECT teachers_id, latitude, longitude, date, groups, subject, semester ' \
                                   'FROM public.teachers_coordinates ' \
                                   'WHERE teachers_id = %s AND subject = %s ' \
                                   'AND groups LIKE ' + '\'%%\' ' + '|| %s || ' + '\'%%\'; '
        record_tuple = (teacher_id, subject, groups)
        cursor.execute(postgre_sql_select_query, record_tuple)
        mobile_records = cursor.fetchall()
        for row in mobile_records:
            dates.append(row[3])
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error TEACHERS COORDINATES while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()

    # print('-'*40)
    # print(dates)
    # print('-' * 40)
    return dates
