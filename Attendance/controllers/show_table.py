import psycopg2
from django.shortcuts import render

from Attendance.controllers.add.group import get_student_groups
from Attendance.controllers.add.subject import insert_into_subjects
from Attendance.controllers.get.all_groups import groups, group_ids
from Attendance.controllers.get.all_subjects import subjects_many
from Attendance.controllers.get.id import get_teachers_id
from Attendance.controllers.get.number_of_students import Student
from Attendance.controllers.get.sql_connection import get_sql_connection


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    teacher_id = get_teachers_id(str(request.user))
    all_groups = groups(teacher_id)
    st_groups = get_student_groups()
    for group in st_groups:
        all_groups.append(group)

    all_subjects = subjects_many(group_ids(teacher_id))
    print("-" * 40)
    print(all_subjects)
    print("-" * 40)

    all_groups = list(dict.fromkeys(all_groups))
    all_subjects = list(dict.fromkeys(all_subjects))
    return render(request, 'home.html',
                  dict(students=[], groups=all_groups,
                       subjects=all_subjects))


def count_number_os_students(semester, subject, groups):
    print(groups)
    students = []
    try:
        connection = get_sql_connection()
        cursor = connection.cursor()
        postgres_sql_select_query = 'SELECT att.student_id, att.date, att.latitude, att.longitude, st.first_name, ' \
                                    'st.second_name, st."group" FROM public.attendance as att INNER JOIN ' \
                                    'public.students as st ON ' \
                                    'st.student_id=att.student_id AND att.date::timestamp  BETWEEN  %s::timestamp  ' \
                                    'AND  ' \
                                    '%s::timestamp  AND  %s LIKE ' + '\'%%\' ' + '|| st."group" || ' + '\'%%\'; '
        record_tuple = (dates[0], dates[1], groups)
        cursor.execute(postgres_sql_select_query, record_tuple)

        mobile_records = cursor.fetchall()
        number_of_students = 0

        print('^' * 40)
        print(mobile_records)
        print('^' * 40)
        print(postgres_sql_select_query)
        for row in mobile_records:
            st = Student()
            st.number = number_of_students + 1
            st.date = row[1]
            st.latitude = row[2]
            st.longitude = row[3]
            st.first_name = row[4]
            st.second_name = row[5]
            st.group = row[6]
            number_of_students += 1
            students.append(st)

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error count_number_os_students while doing smth in PostgreSQL", error)
        student_or_teacher = 1
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        print("PostgreSQL count_number_os_students connection is closed")
    return students
