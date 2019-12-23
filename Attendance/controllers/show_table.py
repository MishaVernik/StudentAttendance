import datetime

import psycopg2
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response

from Attendance.controllers.add.group import get_student_groups
from Attendance.controllers.get.all_groups import groups, group_ids
from Attendance.controllers.get.all_subjects import subjects_many
from Attendance.controllers.get.id import get_teachers_id
from Attendance.controllers.get.number_of_students import Student
from Attendance.context.sql_connection import get_sql_connection
from datetime import datetime, date, time, timedelta


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
    #print("-" * 40)
    #print(all_subjects)
    #print("-" * 40)

    all_groups = list(dict.fromkeys(all_groups))
    all_subjects = list(dict.fromkeys(all_subjects))
    return render(request, 'home_teacher_show_table.html',
                  dict(students=[], groups=all_groups,
                       subjects=all_subjects, state=[0, 1]))


def show_table(request):
    """
    :param request:
        user -> teachers_id
        subject -> subject
        semester -> semester
        list: groups -> groups
    :return: html render

    TODO:
      --- For Teacher ---
        general_table:
            cols :
                [number, first name, second name, group, date1, ... , dateN]
            rows :
                [1, Misha, Vernik, KV-71, -, +, + , + .... , - ]
                [2, Sasha, Murin, Kv-73, -, +, - , - .... , - ]
                [3, Alex, Rqet, KV-72, -, +, - , + .... , - ]
                [4, Sonya, Upaq, KV-74, -, -, + , + .... , - ]
        1. Write ajax-script to send POST request to the /show_table/
            - subject
            - semester
            - groups[]
            - user
        2. Retrieve these data on the server side
        3. Get teacher_id
        4. Get all teachers dates (lecture dates)
        5. Get all students that connected to the groups that has teacher
        6. Iterate through lecture_dates
            7. Get all students that visited this lecture
            8. Mark them in the general table
        9. Send general table to the HTML
        10. Parse this table in the HTML page code
        11. Put this table in the .CSV file
         --- For Student ---
         1. 2 drop dowm lists
            - semester
            - subject
        2. Button "Show attendance"
            :returns
            - table
                cols:
                    [(date1, +) , (date2, -), ... , (dateN, +)]

    """
    # p.2
    # #print('#'*40)
    # #print(request.user)
    semester = str(request.POST.get('semester')).split()
    subject = str(request.POST.get('subject'))
    lst_tmp = request.POST.getlist('groups[]')
    # #print(subject)
    lst_groups = ','.join(lst_tmp)
    # #print(lst_groups)
    # p.3
    teacher_id = get_teachers_id(str(request.user))
    # p.4
    from Attendance.get.all_teachers import all_dates_t
    all_teacher_dates = all_dates_t(teacher_id=teacher_id, subject=subject, semester=semester, groups=lst_groups)
    # #print('all_teacher_dates : ', all_teacher_dates)
    # p.5
    from Attendance.get.all_students import all_students_s
    all_students = all_students_s(groups=lst_groups)
    # #print('all_students : ', all_students)
    general_table = []
    students_table = {}
    cols = ['Name', 'Group']
    # puts all students - that connected to the lst_groups in the students_table
    for student in all_students:
        students_table[str(student[1]) + " " + str(student[2])] = [student[3]]
    current = 1
    for lecture in all_teacher_dates:
        if intersection_between_2_groups_bool(group1=lecture[1], group2=lst_groups):
            # adds new date to the 'cols'

            #print('cols:', cols)
            current_students_on_lecture = students_on_lecture(lecture[0], lecture[1])
            groups_2 = intersection_between_2_groups_array(lecture[1], lst_groups)
            is_changed = False
            for student in current_students_on_lecture:
                if groups_2.get(student.group, None) == 1:
                    if len(students_table.get(student.first_name + " " + student.second_name, None)) > 0:
                        students_table[student.first_name + " " + student.second_name].append('+')
                        if not is_changed:
                            is_changed = True
                            current += 1
                            cols.append(lecture[0])

            for student, arr in students_table.items():
                if len(arr) != current:
                    arr.append('-')

    all_groups = groups(teacher_id)
    # st_groups = get_student_groups()
    #print('#printing table...')
    # import csv
    # response = HttpResponse(content_type='text/csv')
    # response['Content-Disposition'] = 'attachment; filename="attendance.csv"'
    #
    # #with open('innovators.csv', 'w', newline='') as file:
    # writer = csv.writer(response, delimiter=',')
    # writer.writerow(cols)
    # for student, attendance in students_table.items():
    #     #print(student, attendance)
    #     tmp = attendance
    #     tmp.insert(0, student)
    #     writer.writerow(tmp)
    # return response
    all_subjects = subjects_many(group_ids(teacher_id))

    return render(request, 'home_teacher.html',
                  dict(students=[], groups=all_groups,
                       subject=all_subjects, cols=cols, rows=students_table, state=[0, 1]))


def students_on_lecture(date, st_groups):
    # dates = last_teachers_date()
    global cursor, connection
    date = datetime.strptime(date.split('.')[0], '%Y-%m-%d %H:%M:%S')
    dates = [date, date + timedelta(minutes=20)]
    #print(dates)
    #print(st_groups)
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
        #print(dates[1])
        record_tuple = (dates[0], dates[1], st_groups)
        cursor.execute(postgres_sql_select_query, record_tuple)

        mobile_records = cursor.fetchall()
        number_of_students = 0

        #print('^' * 40)
        #print(mobile_records)
        #print('^' * 40)
        #print(postgres_sql_select_query)
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
        print("Error students_on_lecture while doing smth in PostgreSQL", error)
        student_or_teacher = 1
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        #print("PostgreSQL count_number_os_students connection is closed")
    return students


def intersection_between_2_groups_bool(group1, group2):
    groups_1 = str(group1).split(',')
    groups_2 = str(group2).split(',')
    dct_1 = {}
    for group in groups_1:
        dct_1[group] = 1
    for group in groups_2:
        if dct_1.get(group, None) == 1:
            return True

    return False


def intersection_between_2_groups_array(group1, group2):
    ans = {}
    groups_1 = group1.split(',')
    groups_2 = group2.split(',')
    dct_1 = {}
    for group in groups_1:
        dct_1[group] = 1
    for group in groups_2:
        if dct_1.get(group, None) == 1:
            ans[group] = 1

    return ans
