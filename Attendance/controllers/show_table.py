import psycopg2
from django.shortcuts import render

from Attendance.controllers.add.group import get_student_groups
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
    return render(request, 'home.html',
                  dict(students=[], groups=all_groups,
                       subjects=all_subjects))
