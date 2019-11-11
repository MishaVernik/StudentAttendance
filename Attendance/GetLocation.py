from datetime import datetime, timedelta

import psycopg2
from django.shortcuts import render

from Attendance.CheckIfStudentOnTheLecture import ifStudentOnTheLecture
from Attendance.GetId import getStudentsId
from Attendance.CalculateDistance import calcLocationDiff


def getTeachersLocation(request):
    # Get teachers Id
    teacher_id = 0
    print(request.POST['email'])
    try:
        connection = psycopg2.connect(user="cqwhbabxmaxxqd",
                                      password="a3063dc5aeec69b41564cd0f1e3c698e0ff9653385f3b87c0f113b70951eb5b3",
                                      host="ec2-54-235-92-244.compute-1.amazonaws.com",
                                      port="5432",
                                      database="d8d34m4nml4iij")
        cursor = connection.cursor()
        email = request.POST['email']
        postgreSQL_select_Query = "SELECT * FROM public.teachers WHERE public.teachers.email=%s"
        cursor.execute(postgreSQL_select_Query, (email,))
        mobile_records = cursor.fetchall()
        for row in mobile_records:
            teacher_id = row[0]

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
    try:
        connection = psycopg2.connect(user="cqwhbabxmaxxqd",
                                      password="a3063dc5aeec69b41564cd0f1e3c698e0ff9653385f3b87c0f113b70951eb5b3",
                                      host="ec2-54-235-92-244.compute-1.amazonaws.com",
                                      port="5432",
                                      database="d8d34m4nml4iij")

        cursor = connection.cursor()

        create_table_query = ''' INSERT INTO public.teachers_coordinates(
                           teachers_id, "date", latitude, longitude)
                            VALUES (%s, %s, %s, %s);
                              '''

        recordTuple = (teacher_id, datetime.now(), request.POST['latitude'], request.POST['longitude'])
        cursor.execute(create_table_query, recordTuple)
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()

    return render(request, 'homeTeacher.html')

def getStudentsLocation(request):
    # Get teachers Id
    print(request.user)
    student_id = getStudentsId(str(request.user))
    student_arr = []

    dateOriginal = datetime.now()
    datePlus20 = datetime.now()
    # Get last teachers visit
    latitude = 0
    longitude = 0
    try:
        connection = psycopg2.connect(user="cqwhbabxmaxxqd",
                                      password="a3063dc5aeec69b41564cd0f1e3c698e0ff9653385f3b87c0f113b70951eb5b3",
                                      host="ec2-54-235-92-244.compute-1.amazonaws.com",
                                      port="5432",
                                      database="d8d34m4nml4iij")

        cursor = connection.cursor()
        postgreSQL_select_Query = "SELECT teachers_id, date, latitude, longitude FROM public.teachers_coordinates ORDER BY date DESC LIMIT 1"
        cursor.execute(postgreSQL_select_Query)
        mobile_records = cursor.fetchall()

        for row in mobile_records:
            teacher_id = row[0]
            latitude = row[2]
            longitude = row[3]
            dateOriginal = datetime.strptime(row[1].split('.')[0], '%Y-%m-%d %H:%M:%S')
            datePlus20 = datetime.strptime(row[1].split('.')[0], '%Y-%m-%d %H:%M:%S')
        datePlus20 = datePlus20 + timedelta(minutes=20)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error getStudentsLocation while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        print("PostgreSQL getStudentsLocation connection is closed")
    # Check with date now
    # Check location difference between
    present = datetime.now()
    if present > datePlus20 or calcLocationDiff(request.POST['latitude'],request.POST['longitude'], latitude, longitude) == False or ifStudentOnTheLecture(student_id,dateOriginal,datePlus20):
        return render(request, 'home.html')
    try:
        connection = psycopg2.connect(user="cqwhbabxmaxxqd",
                                      password="a3063dc5aeec69b41564cd0f1e3c698e0ff9653385f3b87c0f113b70951eb5b3",
                                      host="ec2-54-235-92-244.compute-1.amazonaws.com",
                                      port="5432",
                                      database="d8d34m4nml4iij")

        cursor = connection.cursor()

        create_table_query = ''' INSERT INTO public.attendance(
                          student_id, date, latitude, longitude)
                            VALUES (%s, %s, %s, %s);
                              '''

        recordTuple = (student_id, datetime.now(), request.POST['latitude'], request.POST['longitude'],)
        cursor.execute(create_table_query, recordTuple)
        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error attendance while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
    return render(request, 'home.html')