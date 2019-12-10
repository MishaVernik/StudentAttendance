import psycopg2

from Attendance.controllers.get.sql_connection import get_sql_connection


# if one element
def subjects_one(schedule_id):
    subject = []
    try:
        connection = get_sql_connection()
        cursor = connection.cursor()
        postgre_sql_select_query = 'SELECT id, subject  FROM public.subjects WHERE schedule_id=%s'
        print(postgre_sql_select_query)
        cursor.execute(postgre_sql_select_query, (schedule_id,))
        mobile_records = cursor.fetchall()
        for row in mobile_records:
            subject.append(row[1])

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error subjects while doing smth in PostgreSQL", error)
        student_or_teacher = 1
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
    return subject


# if array of elements
def subjects_many(schedule_ids):
    all_subjects = []
    for schedule_id in schedule_ids:
        try:
            connection = get_sql_connection()
            cursor = connection.cursor()
            postgre_sql_select_query = 'SELECT id, subject  FROM public.subjects WHERE schedule_id=%s'
            print(postgre_sql_select_query)
            cursor.execute(postgre_sql_select_query, (schedule_id,))
            mobile_records = cursor.fetchall()
            for row in mobile_records:
                all_subjects.append(row[1])

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error subjects while doing smth in PostgreSQL", error)
            student_or_teacher = 1
        finally:
            # closing database connection.
            cursor.close()
            connection.close()
    return all_subjects
