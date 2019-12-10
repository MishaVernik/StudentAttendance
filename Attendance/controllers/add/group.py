import psycopg2
from django.shortcuts import render

from Attendance.controllers.add.subject import insert_into_subjects
from Attendance.controllers.get.all_groups import groups, group_ids
from Attendance.controllers.get.all_subjects import subjects_many
from Attendance.controllers.get.id import get_teachers_id
from Attendance.controllers.get.sql_connection import get_sql_connection
from Attendance.views import home_teacher


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    teacher_id = get_teachers_id(str(request.user))
    all_groups = groups(teacher_id)
    all_subjects = subjects_many(group_ids(teacher_id))
    print("-" * 40)
    print(all_subjects)
    print("-" * 40)

    set_all_groups = set(all_groups)
    set_all_subjects = set(all_subjects)
    all_groups = list(set_all_groups)
    all_subjects = list(set_all_subjects)
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
        print("Error ifStudentOnTheLecture while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        print("PostgreSQL ifStudentOnTheLecture connection is closed")
    return -1


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
    return home_teacher(request)
