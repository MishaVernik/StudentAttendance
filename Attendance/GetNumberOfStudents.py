import psycopg2

from Attendance.GetTeachersDate import getLastTeachersDate


def countNumberOsStudents():
    dates = getLastTeachersDate()
    try:
        connection = psycopg2.connect(user="cqwhbabxmaxxqd",
                                      password="a3063dc5aeec69b41564cd0f1e3c698e0ff9653385f3b87c0f113b70951eb5b3",
                                      host="ec2-54-235-92-244.compute-1.amazonaws.com",
                                      port="5432",
                                      database="d8d34m4nml4iij")

        cursor = connection.cursor()

        postgreSQL_select_Query = "SELECT COUNT(*) FROM public.attendance WHERE  date <= %s::date AND  date >= %s::date;"

        cursor.execute(postgreSQL_select_Query, (dates[1]), (dates[0]))
        print("Selecting ifStudentOnTheLecture rows from mobile table using cursor.fetchall")
        mobile_records = cursor.fetchall()
        number_of_students = 0
        for row in mobile_records:
            number_of_students = row[0]
        return number_of_students
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error ifStudentOnTheLecture while doing smth in PostgreSQL", error)
        student_or_teacher = 1
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
        print("PostgreSQL ifStudentOnTheLecture connection is closed")
    return 0