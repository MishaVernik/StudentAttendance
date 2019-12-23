import psycopg2

from Attendance.context.sql_connection import get_sql_connection


# Gets all students by subject and group
def all_students_s(groups):
    global connection, cursor
    '''
        @:param students
         - array of students data set
            [student_id,first_name, second_name, group]            
    '''
    #print(groups)
    students = []
    try:
        connection = get_sql_connection()
        cursor = connection.cursor()
        postgre_sql_select_query = 'SELECT st.student_id,st.first_name, st.second_name, st.username, st.email, ' \
                                   'st."group", st.github ' \
                                   'FROM public.students as st ' \
                                   'WHERE ' \
                                   "%s  LIKE " + '\'%%\' ' + ' ||  st."group" || ' + '\'%%\';'
        record_tuple = (groups,)
        cursor.execute(postgre_sql_select_query, record_tuple)
        mobile_records = cursor.fetchall()
        for row in mobile_records:
            students.append([row[0], row[1], row[2], row[5]])
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error all_students while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
    #print('-' * 40)
    #print(students)
    #print('-' * 40)
    return students
