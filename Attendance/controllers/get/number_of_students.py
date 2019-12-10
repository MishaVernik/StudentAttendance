import json
from json import JSONEncoder

import psycopg2

from Attendance.controllers.get.sql_connection import get_sql_connection
from Attendance.controllers.get.teachers_date import get_last_teachers_date


class StudentEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Student):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


class Student(JSONEncoder):
    def default(self, o):
        return o.__dict__

    def __init__(self):
        self._number = 0
        self._first_name = ""
        self._second_name = ""
        self._group = ""
        self._latitude = ""
        self._longitude = ""
        self._date = ""

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        self._number = value

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, value):
        self._group = value

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        self._latitude = value

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        self._longitude = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def second_name(self):
        return self._second_name

    @second_name.setter
    def second_name(self, value):
        self._second_name = value

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = value


def count_number_os_students():
    dates = get_last_teachers_date()
    print(dates)
    students = []
    try:
        connection = get_sql_connection()
        cursor = connection.cursor()
        postgres_sql_select_query = 'SELECT att.student_id, att.date, att.latitude, att.longitude, st.first_name, ' \
                                    'st.second_name, st."group" FROM public.attendance as att INNER JOIN ' \
                                    'public.students as st ON ' \
                                    'st.student_id=att.student_id AND att.date::date BETWEEN  %s::date AND  ' \
                                    '%s::date; '
        print(postgres_sql_select_query)
        cursor.execute(postgres_sql_select_query, (dates[1], dates[0]), )

        mobile_records = cursor.fetchall()
        number_of_students = 0
        print(mobile_records)

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
        print("Error ifStudentOnTheLecture while doing smth in PostgreSQL", error)
        student_or_teacher = 1
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        print("PostgreSQL ifStudentOnTheLecture connection is closed")
    return students
