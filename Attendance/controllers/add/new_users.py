import psycopg2

from Attendance.context.sql_connection import get_sql_connection


def add_student(first_name, second_name, group, email, github, username, password):
    try:
        connection = get_sql_connection()
        cursor = connection.cursor()
        create_table_query = ''' INSERT INTO public.students(
                            first_name, second_name, email, "group", github, password, username)
                            VALUES (%s, %s, %s, %s, %s, %s, %s);
                              '''
        record_tuple = (first_name, second_name, email, group, github, password, username)
        cursor.execute(create_table_query, record_tuple)
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()


def add_schedule(teacher_id, groups, name):
    try:
        connection = get_sql_connection()

        cursor = connection.cursor()
        arr_groups = groups.split(',')
        print(arr_groups)
        for group in arr_groups:
            print(group)
            create_table_query = ''' INSERT INTO public.schedule(
                               teacher_id, "group", name)
                                VALUES (%s, %s, %s);
                                  '''
            record_tuple = (teacher_id, str(group), str(name))
            cursor.execute(create_table_query, record_tuple)
            connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()


def add_teacher(first_name, second_name, groups, email, faculty, username, password):
    try:
        connection = get_sql_connection()
        cursor = connection.cursor()
        create_table_query = ''' INSERT INTO public.teachers(
                            first_name, second_name, email, faculty, password, username)
                            VALUES (%s, %s, %s, %s, %s, %s);
                              '''

        record_tuple = (first_name, second_name, email,  faculty, password, username)
        cursor.execute(create_table_query, record_tuple)
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()

    teacher_id = 0
    try:
        connection = get_sql_connection()
        cursor = connection.cursor()
        postgre_sql_select_query = "SELECT teacher_id FROM public.teachers ORDER BY teacher_id DESC LIMIT 1"
        cursor.execute(postgre_sql_select_query)
        mobile_records = cursor.fetchall()
        for row in mobile_records:
            teacher_id = row[0]

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
    add_schedule(teacher_id, groups, "SQL")