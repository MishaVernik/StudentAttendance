import psycopg2


def add_student(first_name, second_name, group, email, github, username, password):
    try:
        connection = psycopg2.connect(user="cqwhbabxmaxxqd",
                                      password="a3063dc5aeec69b41564cd0f1e3c698e0ff9653385f3b87c0f113b70951eb5b3",
                                      host="ec2-54-235-92-244.compute-1.amazonaws.com",
                                      port="5432",
                                      database="d8d34m4nml4iij")
        cursor = connection.cursor()
        create_table_query = ''' INSERT INTO public.students(
                            first_name, second_name, email, "group", github, password, username)
                            VALUES (%s, %s, %s, %s, %s, %s, %s);
                              '''
        recordTuple = (first_name, second_name, email, group, github, password, username)
        cursor.execute(create_table_query, recordTuple)
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()


def add_schedule(teacher_id, groups, name):
    try:
        connection = psycopg2.connect(user="cqwhbabxmaxxqd",
                                      password="a3063dc5aeec69b41564cd0f1e3c698e0ff9653385f3b87c0f113b70951eb5b3",
                                      host="ec2-54-235-92-244.compute-1.amazonaws.com",
                                      port="5432",
                                      database="d8d34m4nml4iij")

        cursor = connection.cursor()
        arr_groups = groups.split(',')
        print(arr_groups)
        for group in arr_groups:
            print(group)
            create_table_query = ''' INSERT INTO public.schedule(
                               teacher_id, "group", name)
                                VALUES (%s, %s, %s);
                                  '''
            recordTuple = (teacher_id, str(group), str(name))
            cursor.execute(create_table_query, recordTuple)
            connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()


def add_teacher(first_name, second_name, groups, email, faculty, username, password):
    try:
        connection = psycopg2.connect(user="cqwhbabxmaxxqd",
                                      password="a3063dc5aeec69b41564cd0f1e3c698e0ff9653385f3b87c0f113b70951eb5b3",
                                      host="ec2-54-235-92-244.compute-1.amazonaws.com",
                                      port="5432",
                                      database="d8d34m4nml4iij")
        cursor = connection.cursor()
        create_table_query = ''' INSERT INTO public.teachers(
                            first_name, second_name, email, faculty, password, username)
                            VALUES (%s, %s, %s, %s, %s, %s);
                              '''

        recordTuple = (first_name, second_name, email,  faculty, password, username)
        cursor.execute(create_table_query, recordTuple)
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()

    teacher_id = 0
    try:
        connection = psycopg2.connect(user="cqwhbabxmaxxqd",
                                      password="a3063dc5aeec69b41564cd0f1e3c698e0ff9653385f3b87c0f113b70951eb5b3",
                                      host="ec2-54-235-92-244.compute-1.amazonaws.com",
                                      port="5432",
                                      database="d8d34m4nml4iij")
        cursor = connection.cursor()
        postgreSQL_select_Query = "SELECT teacher_id FROM public.teachers ORDER BY teacher_id DESC LIMIT 1"
        cursor.execute(postgreSQL_select_Query)
        mobile_records = cursor.fetchall()
        for row in mobile_records:
            teacher_id = row[0]

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while doing smth in PostgreSQL", error)
    finally:
        # closing database connection.
        cursor.close()
        connection.close()
    add_schedule(teacher_id, groups, "SQL")