import json
from builtins import str

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from Attendance.controllers.add.group import get_student_groups
from Attendance.controllers.add.new_users import add_student, add_teacher
from Attendance.controllers.check_if_student_on_the_lecture import if_student_on_the_lecture
from Attendance.controllers.get.all_groups import groups, group_ids
from Attendance.controllers.get.all_subjects import subjects_many
from Attendance.controllers.get.id import get_students_id, get_teachers_id
from Attendance.controllers.get.number_of_students import count_number_os_students
from Attendance.controllers.get.students_group import students_group
from Attendance.forms import SignUpStudentForm, SignUpTeacherForm
from datetime import datetime, timedelta

from Attendance.get.latest_teachers_date import get_latest_teachers_date


@login_required
def home(request):
    # var place
    student_id = get_students_id(str(request.user))
    teacher_id = get_teachers_id(str(request.user))
    student_or_teacher = 0

    if student_id == 0:
        student_or_teacher = 1

    test_date = datetime.now()
    date_plus20 = test_date
    date_original = test_date
    semester = -1
    subject = ""
    _groups = ""
    _groups, date_original, date_plus20 = get_latest_teachers_date(_groups, date_original, date_plus20)
    if student_or_teacher == 1:
        st = count_number_os_students()
        json_st = []
        for el in st:
            json_st.append(el.number)
            json_st.append(el.first_name + " " + el.second_name)
            json_st.append(el.latitude)
            json_st.append(el.longitude)

        teacher_id = get_teachers_id(str(request.user))
        all_groups = groups(teacher_id)
        st_groups = get_student_groups()
        for group in st_groups:
            ##print(group)
            all_groups.append(group)
        all_subjects = subjects_many(group_ids(teacher_id))

        all_groups = list(dict.fromkeys(all_groups))
        all_subjects = list(dict.fromkeys(all_subjects))
        # ##print('-'*400)
        return render(request, 'home_teacher.html',
                      dict(content=[len(st), ], students=st, json_st=json.dumps(json_st), groups=all_groups,
                           subjects=all_subjects, state=[2]))

    present = datetime.now()
    if (present > date_plus20) or if_student_on_the_lecture(student_id, date_original,
                                                            date_plus20) or test_date + timedelta(
        minutes=20) == date_plus20 or students_group(str(request.user)) not in _groups:
        return render(request, 'home.html')
    return render(request, 'home_student_location.html')


def convert_lst_to_dict(lst):
    res_dict = {}
    ##print(lst)
    for cnt, el in enumerate(lst):
        ##print(el, cnt)
        el = el + '-' + str(cnt)
        res_dict[el] = cnt
    # res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dict


@login_required
def home_teacher(request):
    content = [' ']  # convert_lst_to_dict()
    st = count_number_os_students()
    #print('#' * 40)
    json_st = []
    for el in st:
        json_st.append(el.number)
        json_st.append(el.first_name + " " + el.second_name)
        json_st.append(el.latitude)
        json_st.append(el.longitude)

    teacher_id = get_teachers_id(str(request.user))
    all_groups = groups(teacher_id)
    st_groups = get_student_groups()
    for group in st_groups:
        #print(group)
        all_groups.append(group)

    all_subjects = subjects_many(group_ids(teacher_id))

    all_groups = list(dict.fromkeys(all_groups))
    all_subjects = list(dict.fromkeys(all_subjects))

    return render(request, 'home_teacher.html',
                  dict(content=[len(st), ], students=st, json_st=json.dumps(json_st), groups=all_groups,
                       subjects=all_subjects, state=[2]))


def sign_up_teacher(request):
    if request.method == 'POST':
        form = SignUpTeacherForm(request.POST)
        if form.is_valid():
            form.save()
            # student_or_teacher = request.POST.get('')
            first_name = form.cleaned_data.get('first_name')
            second_name = form.cleaned_data.get('last_name')
            groups = form.cleaned_data.get('groups')
            email = form.cleaned_data.get('email')
            faculty = form.cleaned_data.get('faculty')

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            messages.success(request, f'Account created for {username}')
            login(request, user)
            add_teacher(first_name, second_name, groups, email, faculty, username, raw_password)
            return redirect('/accounts/profile/teacher/')
    else:
        form = SignUpTeacherForm()
    return render(request, 'signup_teacher.html', {'form': form})


def signup_student(request):
    if request.method == 'POST':
        form = SignUpStudentForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            second_name = form.cleaned_data.get('last_name')
            group = form.cleaned_data.get('group')
            email = form.cleaned_data.get('email')
            github = form.cleaned_data.get('github')

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            messages.success(request, f'Account created for {username}')
            login(request, user)

            add_student(first_name, second_name, group, email, github, username, raw_password)
            return redirect('home')
    else:
        form = SignUpStudentForm()
    return render(request, 'signup_student.html', {'form': form})
