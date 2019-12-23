import psycopg2

from Attendance.context.sql_connection import get_sql_connection


def group_ids(teacher_id):
    all_group_ids = []
    try:
        connection = get_sql_connection()
        cursor = connection.cursor()
        postgre_sql_select_query = 'SELECT id, "group"  FROM public.schedule WHERE teacher_id=%s'
        #print(postgre_sql_select_query)
        cursor.execute(postgre_sql_select_query, (teacher_id,))
        mobile_records = cursor.fetchall()
        for row in mobile_records:
            all_group_ids.append(row[0])

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error STUDENTS while doing smth in PostgreSQL", error)
        student_or_teacher = 1
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
    return all_group_ids


def groups(teacher_id):
    all_groups = []
    try:
        connection = get_sql_connection()
        cursor = connection.cursor()
        postgre_sql_select_query = 'SELECT id, "group"  FROM public.schedule WHERE teacher_id=%s'
        #print(postgre_sql_select_query)
        cursor.execute(postgre_sql_select_query, (teacher_id,))
        mobile_records = cursor.fetchall()
        for row in mobile_records:
            all_groups.append(row[1])

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error STUDENTS while doing smth in PostgreSQL", error)
        student_or_teacher = 1
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
    return all_groups
