import psycopg2


def getStudentsId(user1):
    student_id = 0
    try:
        connection = psycopg2.connect(user="cqwhbabxmaxxqd",
                                      password="a3063dc5aeec69b41564cd0f1e3c698e0ff9653385f3b87c0f113b70951eb5b3",
                                      host="ec2-54-235-92-244.compute-1.amazonaws.com",
                                      port="5432",
                                      database="d8d34m4nml4iij")

        cursor = connection.cursor()

        postgreSQL_select_Query = "SELECT student_id, username FROM public.students WHERE username=%s"

        cursor.execute(postgreSQL_select_Query, (user1,))
        print("Selecting STUDENTS rows from mobile table using cursor.fetchall")
        mobile_records = cursor.fetchall()
        print(mobile_records)
        for row in mobile_records:
            student_id = row[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error STUDENTS while doing smth in PostgreSQL", error)
        student_or_teacher = 1
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        print("PostgreSQL STUDENTS connection is closed")

    return student_id


def getTeachersId(username):
    teachers_id = 0
    try:
        connection = psycopg2.connect(user="cqwhbabxmaxxqd",
                                      password="a3063dc5aeec69b41564cd0f1e3c698e0ff9653385f3b87c0f113b70951eb5b3",
                                      host="ec2-54-235-92-244.compute-1.amazonaws.com",
                                      port="5432",
                                      database="d8d34m4nml4iij")

        cursor = connection.cursor()

        postgreSQL_select_Query = "SELECT * FROM public.teachers WHERE username=%s"

        cursor.execute(postgreSQL_select_Query, (username,))
        print("Selecting TEACHERS rows from mobile table using cursor.fetchall")
        mobile_records = cursor.fetchall()
        for row in mobile_records:
            teachers_id = row[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error TEACHERS while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        print("PostgreSQL  TEACHERS connection is closed")
    return teachers_id