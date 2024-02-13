import sqlite3

connection = sqlite3.connect("school.db")
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id int primary key,
lastname TEXT NOT NULL,
firstname TEXT not null,
username TEXT NOT NULL,
password TEXT NOT NULL,
role TEXT NOT NULL,
CONSTRAINT constraint_users UNIQUE (username)
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS Lession (
date TEXT NOT null,
number integer not null,
lession text not null,
CONSTRAINT constraint_name UNIQUE (date, number)
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS Eva (
lastname text not null,
firstname text not null,
date text not null,
lession text not null,
eva integer not null
)
''')
def delete_account(lastname, firstname,username):
    cursor.execute("delete from Users where firstname = ? and lastname = ? and username = ?",(firstname, lastname, username))
    connection.commit()
    exit()
def print_lession():
    cursor.execute("select distinct date from Lession")
    x = cursor.fetchall()
    for line in x:
        print(line[0] + ":\n")
        cursor.execute('select number,lession from Lession where date = ?',(line))
        result = cursor.fetchall()
        for res in result:
            print("\t" + str(res[0]) + " " + res[1] + "\n")
def add_lession(date, number, lession):
    cursor.execute("insert into Lession(date, number, lession) values (?,?,?)",(date,number,lession))
    connection.commit()
def update_lession(date,number, lession):
    cursor.execute("update Lession set lession = ? where date = ? and number = ?", (lession,date,number))
    connection.commit()
def delete_lession(date, number):
    cursor.execute("delete from Lession where date = ? and number = ?",(date,number))
    connection.commit()
def print_eva():
    cursor.execute("select distinct date from eva")
    x = cursor.fetchall()
    for line in x:
        print(line[0] + ":\n")
        cursor.execute('select lastname, firstname, lession, eva from Eva where date = ?', (line))
        result = cursor.fetchall()
        for res in result:
            print("\t" + " " + res[0] + " " + res[1] + " ->tea " + res[2] + ": " + str(res[3]) + "\n")
def add_eva(firstname, lastname, date, lession, eva):
    cursor.execute("insert into Eva(lastname, firstname, date, lession, eva) values (?,?,?,?,?)", (firstname, lastname, date, lession, eva))
    connection.commit()
def update_eva(firstname, lastname, date, lession, eva):
    cursor.execute("update Eva set eva = ? where firstname = ? and lastname = ? and date = ? and lession = ?",(eva,lastname, firstname, date, lession))
    connection.commit()
def delete_eva(firstname, lastname, date, lession):
    cursor.execute("delete from Eva where firstname = ? and lastname = ? and date = ? and lession = ?",(lastname, firstname, date, lession))
    connection.commit()
while True:
    sussed = True
    login = input("Введите логин:")
    cursor.execute('select * from Users')
    x = cursor.fetchall()
    for line in x:
        if line[3] == login:
            password = input("Введите пароль:")
            if line[4] == password:
                print("Авторизация прошла успешно!\n")
                sussed = False
                username = line[3]
                lastname = line[1]
                firstname = line[2]
                role = line[5]

                break
            else:
                print("Неправильный пароль")
                continue
    if not sussed:
        break
    if sussed:
        select = input("Учетная запись не найдена. Добавить её?[y,n]")
        if select == 'y':
            lastname = input("Введите вашу фамилию:")
            firtname = input("Введите ваше имя:")
            username = input("Введите юзернейм:")
            password = input("Придумайте пароль:")
            role = input("Введите вашу роль:")
            cursor.execute('insert into Users(lastname, firstname, username, password, role) values(?,?,?,?,?)',(lastname,firtname,username,password,role))
            connection.commit()
            print("Запись добавлена\n")
            continue
        elif select == 'n':
            continue
        else:
            print("Действие не определено")
while True:
    if role == 'teacher':
        select = 0
        select = int(input("Выберите действие:\n1)Действия с расписанием\n2)Действия с оценками\n3)Выход\n:"))
        if select == 1:
            select = int(input("Выберите действие:\n1)Просмотреть расписание\n2)Добавить расписание\n3)Изменить расписание\n4)Удалить расписание\n:"))
            if select == 1:
                print_lession()
            elif select == 2:
                add_lession(input("Введите Дату:"),int(input("Введите номер урока:")), input("Введите название предмета:"))
            elif select ==3:
                update_lession(input("Введите Дату:"),int(input("Введите номер урока:")), input("Введите название нового предмета:"))
            elif select == 4:
                delete_lession(input("Введите Дату:"),int(input("Введите номер урока:")))
        elif select == 2:
            select = int(input("Выберите действие:\n1)Просмотреть оценки\n2)Добавить оценки\n3)Изменить оценку\n4)Удалить оценку\n:"))
            if select == 1:
                print_eva()
            elif select == 2:
                add_eva(input("Введите фамилию:"),input("Введите имя:"),input("Введите дату:"),input("Введите название предмета:"), int(input("Введите оценку:")))
            elif select == 3:
                cursor.execute("select * from Eva where firstname='Игорь' and lastname='Махачкалов' and date='2020-12-12'")
                x = cursor.fetchall()
                for line in x:
                    print(line)
                update_eva(input("Введите фамилию:"),input("Введите имя:"),input("Введите дату:"),input("Введите название предмета:"), int(input("Введите новую оценку:")))
            elif select == 4:
                delete_eva(input("Введите фамилию:"),input("Введите имя:"),input("Введите дату:"),input("Введите название предмета:"))
        elif select == 3:
            print("Выход..")
            connection.close()
            exit()
        elif select == 4:
            delete_account(lastname, firstname,username)
    elif role == 'student':
        select = int(input("Выберите действие:\n1)Посмотреть расписание\n2)Посмотреть оценки\n:"))
        if select == 1:
            print_lession()
        elif select == 2 :
            print_eva()
        elif select == 3:
            print("Выход..")
            connection.close()
            exit()
        elif select == 4:
            delete_account(lastname, firstname, username)