from datetime import datetime, timedelta

import psycopg2


def getLastTeachersDate():
    try:
        connection = psycopg2.connect(user="cqwhbabxmaxxqd",
                                      password="a3063dc5aeec69b41564cd0f1e3c698e0ff9653385f3b87c0f113b70951eb5b3",
                                      host="ec2-54-235-92-244.compute-1.amazonaws.com",
                                      port="5432",
                                      database="d8d34m4nml4iij")

        cursor = connection.cursor()

        postgreSQL_select_Query = "SELECT * from public.teachers_coordinates ORDER BY date DESC LIMIT 1;"

        cursor.execute(postgreSQL_select_Query)
        print("Selecting ifStudentOnTheLecture rows from mobile table using cursor.fetchall")
        mobile_records = cursor.fetchall()
        datePlus20 = datetime.now()
        dateOriginal = datetime.now()
        for row in mobile_records:
            dateOriginal = datetime.strptime(row[0].split('.')[0], '%Y-%m-%d %H:%M:%S')

        return [dateOriginal, dateOriginal + timedelta(minutes=20)]
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error ifStudentOnTheLecture while doing smth in PostgreSQL", error)
        student_or_teacher = 1
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        print("PostgreSQL ifStudentOnTheLecture connection is closed")
    return ["",""]