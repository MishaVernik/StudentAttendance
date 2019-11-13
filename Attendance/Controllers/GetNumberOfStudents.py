import psycopg2

from Attendance.Controllers.GetSQLConnection import get_sql_connection
from Attendance.Controllers.GetTeachersDate import get_last_teachers_date


def count_number_os_students():
    dates = get_last_teachers_date()
    print(dates)
    try:
        connection = get_sql_connection()

        cursor = connection.cursor()

        postgre_sql_select_query = "SELECT COUNT(*) FROM public.attendance WHERE date::date BETWEEN  %s::date AND  %s::date;"
        cursor.execute(postgre_sql_select_query, (dates[1], dates[0]),)

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
