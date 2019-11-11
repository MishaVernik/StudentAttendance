from datetime import datetime

import psycopg2


def ifStudentOnTheLecture(student_id, dateOriginal, datePlus20):
    try:
        connection = psycopg2.connect(user="cqwhbabxmaxxqd",
                                      password="a3063dc5aeec69b41564cd0f1e3c698e0ff9653385f3b87c0f113b70951eb5b3",
                                      host="ec2-54-235-92-244.compute-1.amazonaws.com",
                                      port="5432",
                                      database="d8d34m4nml4iij")

        cursor = connection.cursor()

        postgreSQL_select_Query = "SELECT * FROM public.attendance WHERE student_id=%s"

        cursor.execute(postgreSQL_select_Query, (student_id,))
        print("Selecting ifStudentOnTheLecture rows from mobile table using cursor.fetchall")
        mobile_records = cursor.fetchall()
        for row in mobile_records:
            student_id = row[0]
            date = datetime.strptime(row[1].split('.')[0], '%Y-%m-%d %H:%M:%S')
            if (date >= dateOriginal and date <= datePlus20):
                return True
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error ifStudentOnTheLecture while doing smth in PostgreSQL", error)
        student_or_teacher = 1
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        print("PostgreSQL ifStudentOnTheLecture connection is closed")
    return False