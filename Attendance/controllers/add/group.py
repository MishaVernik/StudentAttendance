import psycopg2
from django.shortcuts import render

from Attendance.controllers.add.subject import insert_into_subjects
from Attendance.controllers.get.all_groups import groups, group_ids
from Attendance.controllers.get.all_subjects import subjects_many
from Attendance.controllers.get.id import get_teachers_id
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
    return render(request, 'add_group.html',
                  dict(groups=all_groups,
                       subjects=all_subjects))


def get_schedule_id(teacher_id, group, semester):
    global connection, cursor
    try:
        connection = get_sql_connection()
        cursor = connection.cursor()
        postgre_sql_select_query = 'SELECT id from public.schedule WHERE teacher_id=%s AND "group"=%s AND semester=%s;'
        cursor.execute(postgre_sql_select_query, (teacher_id, group, semester), )
        mobile_records = cursor.fetchall()

        for row in mobile_records:
            return row[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error get_schedule_id while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        print("PostgreSQL ifStudentOnTheLecture connection is closed")
    return -1


def get_student_groups():
    global connection, cursor
    all_groups = []
    try:
        connection = get_sql_connection()
        cursor = connection.cursor()
        postgre_sql_select_query = 'SELECT "group" FROM public.students;'
        cursor.execute(postgre_sql_select_query, )
        mobile_records = cursor.fetchall()
        for row in mobile_records:
            all_groups.append(row[0])
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error get_student_groups while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        print("PostgreSQL get_student_groups connection is closed")
    return all_groups


def add_group(request):
    """

    """
    global connection, cursor
    print(request.user)
    semester = str(request.POST.get('semester')).split()
    subject = request.POST.get('subject')
    teacher_id = get_teachers_id(str(request.user))

    groups = str(request.POST.get('group')).split(',')
    for group in groups:
        schedule_id = get_schedule_id(teacher_id=teacher_id, group=group, semester=semester[1])
        try:
            if schedule_id == -1:
                connection = get_sql_connection()
                cursor = connection.cursor()
                create_table_query = ''' INSERT INTO public.schedule(
                                    teacher_id, "group", semester)
                                    VALUES (%s, %s, %s);
                                      '''

                record_tuple = (teacher_id, group, semester[1])
                cursor.execute(create_table_query, record_tuple)
                connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while doing smth in PostgreSQL", error)
        finally:
            # closing database connection.
            cursor.close()
            connection.close()

        if len(subject) > 0:
            schedule_id = get_schedule_id(teacher_id=teacher_id, group=group, semester=semester[1])
            if schedule_id == -1:
                pass
            else:
                insert_into_subjects(schedule_id, subject, semester[1])
    from Attendance.views import home_teacher
    return home_teacher(request)
