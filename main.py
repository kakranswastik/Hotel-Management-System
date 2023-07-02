# Created by Swastik Kakran on 2023 Jun 27, 21:47:32 IST
# Latest update 2023 Jul 1, 23:24:45 IST

import random
import mysql.connector
import datetime

# This gets realtime date and time. Used for storing data in DB (checkin and checkout).
dateTime = datetime.datetime.now().replace(microsecond=0) 

# It connects the python file to a DB called Records in which user data is stored.
# This variables helps to interact wiht it(CRUD).
records = mysql.connector.connect(host='localhost', user='root', password='password', database='Records')

# Used for running queries in DB using SQL
cursor = records.cursor()

#Only execute these lines(23-25) to create tables current_records and total_records used in the program later to store data.
#I already did so I have commented them.
#You must install MySQL first and adjust the connector according to your DB.
# I have already created a DB and connected to it in line 13. If you don't have a DB, refer to MySQL docs to create one.

#cursor.execute('CREATE TABLE total_records(name varchar(20), age integer, aadhar_no bigint, room_no integer, DateTime_of_checkin DATETIME, DateTime_of_checkout DATETIME)')
#records.commit()
#cursor.execute('CREATE TABLE current_records(name varchar(20), age integer, aadhar_no bigint, room_no integer, DateTime_of_checkin DATETIME)')
#records.commit()

# This is used for admin files access
password = 'password@12345'

# This extracts all the room numbers and store them in a list.
cursor.execute("SELECT room_no FROM current_records;")
n = cursor.fetchall()
occupied_rooms = []
for i in n:
    b = i[0]
    occupied_rooms.append(b)

#this extracts all the adhaar numbers and store them in a list. Used to avoid duplication of data in DB.
cursor.execute("SELECT aadhar_no FROM current_records;")
s = cursor.fetchall()
aadhar = []
for i in s:
    a = i[0]
    aadhar.append(a)

#total number of rooms are 50
# returns a room no. which is not occupied
#function iterates itself until a non-occupied room number is given
def validRoom():
    if len(occupied_rooms) == 50:
        return "full"
    
    else:
        room = random.randint(1, 50)
        for i in occupied_rooms:
            if i == room:
                validRoom()
        else:
            return room

#This function calculates the difference between 2 dates and returns the bill for the stay.
# The bill is calculated per hours. The cost of per hour in Hotel is rs200.
def Bill(d1, d2):
    difference =  d2 - \
        d1
    print("You stayed in Hotel for ", difference,)
    hours_between = difference.total_seconds() / 3600
    bill = hours_between * 200
    total_bill = round(bill, 2)
    return total_bill


def Booking():
    room_no = validRoom()
    if room_no == 'full':
        print("\nHotel is full! All rooms are occupied.")
        print('Sorry for your inconvenience.\n')

    else:    
        name = input('Enter your name: ')
        age = input('Enter your age: ')
        aadhar_no = int(input('Enter your aadhar card number: '))

        if aadhar_no in aadhar:
        #checks if customer is already checked-in or not
            print('\nAadhar already in use! Customer already exists.\n')
        else:
        # Stores the data entered by the user in a tuple and insert it into table by executing query.
            data = (name, age, aadhar_no, room_no, dateTime)
            s = "INSERT INTO current_records (name, age, aadhar_no, room_no, DateTime_of_checkin) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(s, data)
            records.commit()
            print("\n Your room number is ", room_no)
            print('\nThank you for choosing us. Happy stay!\n')


def Service():
    
    your_room = int(input('Enter your room number: '))
    if your_room in occupied_rooms:
        services = input('''Select the service your want: 
1. Room cleaning
2. Food
''')
        if services == '1':
            print('We will send cleaning staff to your room in 5 minutes. Please wait.')
        elif services == '2':
            print('Menu card will be delivered to your room.')
        else:
            print("Enter valid option!")

    else:
        print('Room is not occupied. Enter valid room number.')

def Checkout():
    room = int(input("Enter your room number: "))
    if room in occupied_rooms:
        cursor.execute(f'SELECT * FROM current_records WHERE room_no = "{room}"')
        query = cursor.fetchall()
        query = query[0]
        print(f'''
Name: {query[0]}
age: {query[1]}
aadhar card number: {query[2]}
room number: {room}''')
        user_checkout = input('Do you confirm your check-out? (Y/y for yes, N/n for no): ')

        if user_checkout == 'Y' or user_checkout == 'y':
            cursor.execute(f"SELECT DateTime_of_checkin FROM current_records WHERE room_no = '{room}'")
            date = cursor.fetchall()
            for i in date:
                date_of_checkin = i[0]
            current_datetime = datetime.datetime.now().replace(microsecond=0)
            bill = Bill(date_of_checkin, current_datetime)
            print("\nYour total bill is Rs.", bill)
            print("\nThank you for your stay. Hope you had a great time.\n")

# Now the customer data will be saved in total records and will be deleted from current_records
# current_records hold the info of current customers until they checkout.
# total_records hold the info of all the customers after they checkout.

            new_query = (*query, current_datetime)
            s = "INSERT INTO total_records (name, age, aadhar_no, room_no, DateTime_of_checkin, DateTime_of_checkout) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(s, new_query)
            cursor.execute(f"DELETE FROM current_records WHERE room_no='{room}'")
            records.commit()

        elif user_checkout == 'N' or user_checkout == 'n':
            print("Check-out cancelled.")

        else:
            print("Enter valid option.")

    else:
        print("\nPlease enter correct room number!\n")


while True:
    print('''
-------------------------------------------------------------
                WELCOME TO HOTEL TRANSYLVANIA
-------------------------------------------------------------

Please choose an option:
1. Room Booking
2. Room services
3. Checkout
4. Admin (not for customers)
5. Exit''')
    user_input = int(input('> '))

    if user_input == 1:
        Booking()

# These lines are repeated to update occupied_rooms and aadhar_no after new booking
# Functions are not used as functions are not iterable
# This extracts all the room numbers and store them in a list.
        cursor.execute("SELECT room_no FROM current_records;")
        n = cursor.fetchall()
        occupied_rooms = []
        for i in n:
            b = i[0]
            occupied_rooms.append(b)

#this extracts all the adhaar numbers and store them in a list. Used to avoid duplication of data in DB.
        cursor.execute("SELECT aadhar_no FROM current_records;")
        s = cursor.fetchall()
        aadhar = []
        for i in s:
            a = i[0]
            aadhar.append(a)

    elif user_input == 2:
        Service()

    elif user_input == 3:
        Checkout()
# These lines are repeated to update occupied_rooms and aadhar_no after someone check-outs
# Functions are not used as functions are not iterable
# This extracts all the room numbers and store them in a list.
        cursor.execute("SELECT room_no FROM current_records;")
        n = cursor.fetchall()
        occupied_rooms = []
        for i in n:
            b = i[0]
            occupied_rooms.append(b)

#this extracts all the adhaar numbers and store them in a list. Used to avoid duplication of data in DB.
        cursor.execute("SELECT aadhar_no FROM current_records;")
        s = cursor.fetchall()
        aadhar = []
        for i in s:
            a = i[0]
            aadhar.append(a)

    elif user_input == 4:
        passwd = input('Enter password to access admin files: ')

        if passwd == password:
            while True:
                admin_input = int(input('''
Welcome Admin. Please select an option from below:

1. Display current records
2. Display total records
3. Exit
> '''))
                if admin_input == 1:
                # Fetches the data from the table and store it in rec1 variable.
                # then print it by iterating through rec1
                    cursor.execute("SELECT * FROM current_records;")
                    rec1 = cursor.fetchall()
                    for i in rec1:
                        print(i)

                elif admin_input == 2:
                # Fetches the data from the table and store it in rec2 variable.
                # then print it by iterating through rec2
                    cursor.execute("SELECT * FROM total_records;")
                    rec2 = cursor.fetchall()
                    for i in rec2:
                        print(i)

                elif admin_input == 3:
                    break

                else:
                    print('Enter vaid option!')
        
        else:
            print('Invalid password!')

    elif user_input == 5:
        print('Thank you for your precious time. Have a nice day!')
        break

    else:
        print('Enter valid option!')
