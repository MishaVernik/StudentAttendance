from datetime import datetime, timedelta

import psycopg2

from Attendance.context.sql_connection import get_sql_connection


def get_latest_teachers_date(_groups, date_original, date_plus20):
    try:
        connection = get_sql_connection()
        cursor = connection.cursor()
        postgre_sql_select_query = 'SELECT teachers_id, date, latitude, longitude, semester, subject, groups  FROM ' \
                                   'public.teachers_coordinates ' \
                                   "ORDER BY date DESC LIMIT 1 "
        cursor.execute(postgre_sql_select_query)
        mobile_records = cursor.fetchall()
        for row in mobile_records:
            date_original = datetime.strptime(row[1].split('.')[0], '%Y-%m-%d %H:%M:%S')
            date_plus20 = datetime.strptime(row[1].split('.')[0], '%Y-%m-%d %H:%M:%S')
            semester = row[4]
            subject = row[5]
            _groups = row[6]

        date_plus20 = date_plus20 + timedelta(minutes=20)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error TEACHERS COORDINATES while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
    return _groups, date_original, date_plus20