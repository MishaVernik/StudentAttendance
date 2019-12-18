import psycopg2
from django.shortcuts import render

from Attendance.controllers.get.all_groups import groups, group_ids
from Attendance.controllers.get.all_subjects import subjects_many
from Attendance.controllers.get.id import get_teachers_id
from Attendance.context.sql_connection import get_sql_connection


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    teacher_id = get_teachers_id(str(request.user))
    from Attendance.controllers.add.group import get_student_groups
    all_groups = groups(teacher_id)
    st_groups = get_student_groups()
    for group in st_groups:
        print(group)
        all_groups.append(group)
    all_subjects = subjects_many(group_ids(teacher_id))
    print("-" * 40)
    print(all_subjects)
    print("-" * 40)

    all_groups = list(dict.fromkeys(all_groups))
    all_subjects = list(dict.fromkeys(all_subjects))
    return render(request, 'add_subject.html',
                  dict(groups=all_groups,
                       subjects=all_subjects))


def insert_into_subjects(schedule_id, subject, semester):
    global cursor, connection
    print('INSERTING SUBJECTS')
    try:
        connection = get_sql_connection()
        cursor = connection.cursor()
        create_table_query = ''' INSERT INTO public.subjects(
                            schedule_id, subject, semester)
                            VALUES (%s, %s, %s);
                              '''

        record_tuple = (schedule_id, subject, semester)
        cursor.execute(create_table_query, record_tuple)
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()


def add_subject(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    global cursor, connection
    print(request.user)
    semester = str(request.POST.get('semester')).split()
    subject = request.POST.get('subject')
    teacher_id = get_teachers_id(str(request.user))
    lst_groups = request.POST.getlist('groups')
    for group in lst_groups:
        from Attendance.controllers.add.group import get_schedule_id
        schedule_id = get_schedule_id(teacher_id=teacher_id, group=group, semester=semester[1])
        try:
            connection = get_sql_connection()
            cursor = connection.cursor()
            if schedule_id == -1:
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
