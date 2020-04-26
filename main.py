import sqlite3

database_name = 'school.sqlite.db'


def connect():
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT,name  text,email  text,year  integer)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY AUTOINCREMENT,name  text,max_students  text)")
    cur.execute("CREATE TABLE IF NOT EXISTS tests ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "course_id integer,"
                "name  text,"
                "max_students  text, constraint fk_course foreign key(course_id) references courses(id))")
    cur.execute("CREATE TABLE IF NOT EXISTS student_course ("
                "student_id integer,"
                "course_id integer,"
                "foreign key(student_id) references students(id),"
                "foreign key(course_id) references courses(id))")
    conn.commit()
    conn.close()


def insert_std(name, email, year):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute("INSERT INTO students VALUES(NULL,?,?,?)", (name, email, year))
    conn.commit()
    conn.close()


def get_std_by_id(id_):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute("Select * from students where id = ?", (id_,))
    rows = cur.fetchall()
    conn.close()
    return rows


def insert_course(name, max_std):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute("INSERT INTO courses VALUES(NULL,?,?)", (name, max_std))
    conn.commit()
    conn.close()


def view_courses():
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute("Select * from courses")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_course_by_id(id_):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute("Select * from courses where id = ?", (id_,))
    rows = cur.fetchall()
    conn.close()
    return rows


def insert_test(course_id, name, max_std):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute("INSERT INTO tests VALUES(NULL,?,?,?)", (course_id, name, max_std))
    conn.commit()
    conn.close()


def insert_std_course(std_id, course_id):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute("INSERT INTO student_course VALUES(?,?)", (std_id, course_id))
    conn.commit()
    conn.close()


def last_entry_std():
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute("SELECT * FROM students where id = (SELECT MAX(ID)  FROM students)")
    rows = cur.fetchall()
    conn.close()
    return rows


def last_entry_course():
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute("SELECT * FROM courses where id = (SELECT MAX(ID)  FROM courses)")
    rows = cur.fetchall()
    conn.close()
    return rows


def last_entry_test():
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute("SELECT * FROM tests where id = (SELECT MAX(ID)  FROM tests)")
    rows = cur.fetchall()
    conn.close()
    return rows


def list_courses_by_std_id(std_id):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM courses where id in (select course_id from student_course where student_id = ?) order by id asc ",
        (std_id,))
    # cur.execute("SELECT * FROM student_course")
    rows = cur.fetchall()
    conn.close()
    return rows


def list_test_by_course_id(course_id):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    cur.execute("SELECT * FROM tests where course_id = ? order by id ",
                (course_id,))
    # cur.execute("SELECT * FROM student_course")
    rows = cur.fetchall()
    conn.close()
    return rows


def main():
    choice = 0

    while choice != 7:
        print('1 Add student\n'
              '2 Add course\n'
              '3 Add test\n'
              '4 Add student to course\n'
              '5 List courses by student\n'
              '6 List tests by course\n'
              '7 Exit\n')
        choice = int(input("Input:"))
        if choice == 1:
            name = input("\nEnter Name: ")
            email = input("\nEnter Email: ")
            year = int(input("\nEnter Year: "))

            insert_std(name, email, year)
            for row in last_entry_std():
                # print(
                #     'Added student: id: ' + str(row[0]) + ', name: ' + row[1] + ', email: ' + row[2] + ', year: ' + str(
                #         row[3]))
                print("Added student with id " + str(row[0]))
        if choice == 2:
            name = input("\nEnter courseName: ")
            max_std = input("\nEnter Max students in course: ")
            insert_course(name, max_std)
            for row in last_entry_course():
                # print(
                #     'Added student: id: ' + str(row[0]) + ', name: ' + row[1] + ', email: ' + row[2] + ', year: ' + str(
                #         row[3]))
                print("Added course with id " + str(row[0]))
        if choice == 3:
            name = input("\nEnter Test Name: ")
            course_id = input("\nEnter Course Id:")
            date_time = input("\nEnter Date and time: ")
            if get_course_by_id(course_id):
                insert_test(course_id, name, date_time)
                for row in last_entry_test():
                    # print(
                    #     'Added student: id: ' + str(row[0]) + ', name: ' + row[1] + ', email: ' + row[2] + ', year: ' + str(
                    #         row[3]))
                    print("Added test with ID with id " + str(row[0]))
            else:
                print("Invalid CourseID")
        if choice == 4:
            std_id = input("\nEnter Student ID: ")
            course_id = input("\nEnter Course Id:")
            if get_course_by_id(course_id):
                if get_std_by_id(std_id):
                    insert_std_course(std_id, course_id)
                    print("Added student to course id " + course_id)
                else:
                    print("Student not found")
            else:
                print("Course not found")
        if choice == 5:
            std_id = input("\nEnter Student ID: ")
            if get_std_by_id(std_id):
                data = list_courses_by_std_id(std_id)
                # print(data)
                count = 0
                comma = ' '
                final = ''
                for c in data:
                    if count > 0:
                        comma = ', '
                    final = final + comma + c[1]
                    count += 1
                print('Courses for student ' + str(std_id) + ': ' + final)
            else:
                print('Student not found')
        if choice == 6:
            course_id = input("\nEnter Course Id:")
            if get_course_by_id(course_id):
                data = list_test_by_course_id(course_id)
                # print(data)
                count = 0
                comma = ' '
                final = ''
                for c in data:
                    if count > 0:
                        comma = ', '
                    final = final + comma + c[2]
                    count += 1
                print('Tests for course ' + str(course_id) + ': ' + final)
            else:
                print('Course not found')


if __name__ == '__main__':
    connect()
    main()
