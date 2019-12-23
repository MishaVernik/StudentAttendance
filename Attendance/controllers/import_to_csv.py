from django.http import HttpResponse
from django.shortcuts import render

from Attendance.controllers.add.group import get_student_groups
from Attendance.controllers.get.all_groups import groups, group_ids
from Attendance.controllers.get.all_subjects import subjects_many
from Attendance.controllers.get.id import get_teachers_id


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
    return render(request, 'home.html',
                  dict(groups=all_groups,
                       subjects=all_subjects))


def download_csv(request):
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
        from Attendance.controllers.show_table import intersection_between_2_groups_bool
        if intersection_between_2_groups_bool(group1=lecture[1], group2=lst_groups):
            # adds new date to the 'cols'
            cols.append(lecture[0])
            #print('cols:', cols)
            from Attendance.controllers.show_table import students_on_lecture
            current_students_on_lecture = students_on_lecture(lecture[0], lecture[1])
            from Attendance.controllers.show_table import intersection_between_2_groups_array
            groups_2 = intersection_between_2_groups_array(lecture[1], lst_groups)
            is_changed = False
            for student in current_students_on_lecture:
                if groups_2.get(student.group, None) == 1:
                    if len(students_table.get(student.first_name + " " + student.second_name, None)) > 0:
                        students_table[student.first_name + " " + student.second_name].append('+')
                        if not is_changed:
                            is_changed = True
                            current += 1

            for student, arr in students_table.items():
                if len(arr) != current:
                    arr.append('-')

    all_groups = groups(teacher_id)
    # st_groups = get_student_groups()
    #print('#printing table...')
    import csv
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance.csv"'
    response.write(u'\ufeff'.encode('utf8'))

    # with open('innovators.csv', 'w', newline='') as file:
    writer = csv.writer(response, delimiter=',')
    writer.writerow(cols)
    for student, attendance in students_table.items():
        #print(student, attendance)
        tmp = attendance
        tmp.insert(0, student.encode("utf-8"))
        writer.writerow(tmp)
    return response
