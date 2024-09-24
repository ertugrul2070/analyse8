from db import connect_db
from logging import decrypt_message
import re

def checkFirstName():
    while True:
        print("Only letters and less then 100 characters")
        x = input("Enter First Name: ")
        if len(x) >= 1 and len(x) <= 100 and x.isalpha():
            return x
        else:
             print("-Invalid firstname-")
        
def checkLastName():
    while True:
        print("Only letters and less then 100 characters")
        x = input("Enter Last Name: ")
        if len(x) >= 1 and len(x) <= 100 and x.isalpha():
            return x
        else:
            print("-Invalid lastname-")
        
def checkUserName():
    while True:
        print("Min 8 and max 10 characters long. Can start with `_` and can contain numbers, underscores, apostrophes, and periods")
        x = input("Enter Username: ")
        if re.match(r"^[a-zA-Z_][a-zA-Z0-9_'.]{7,9}$", x):
            if not checkIfUsernameExists(x):
                return x
            else:
                print("-Username already exists-")
        else:
            print("-Invalid username-")

def checkPassword():
    while True:
        print("Min 12 and max 30 characters. contain at least one lowercase letter, one uppercase letter, one digit, and one special character")
        x = input("Enter password: ")
        if re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_\-+=`|\(){}[\]:;\'<>,.?/]).{12,30}$', x):
            return x
        else:
            print("-Invalid password-")

def checkAge():
    while True:
        print("between 16 and 149")
        x = input("Enter age: ")
        try:
            age = int(x)
            if age > 15 and age < 149:
                return age
            else:
                print("- Invalid age. Age must be between 16 and 149 -")
        except ValueError:
            print("- Invalid input. Please enter a valid number -")

def checkGender():
    while True:
        print("Male / Female")
        x = input("Enter gender: ")
        if x == "Male" or x == "Female":
            return x
        else:
            print("-Invalid gender-")

def checkWeight():
    while True:
        print("Weight (Use dot and max 2 numbers after decimal)")
        x = input("Enter weight: ")

        try:
            weight = float(x)
            if '.' in x:
                decimal_part = x.split('.')[1]
                if len(decimal_part) > 2:
                    print("- Invalid weight. Only 2 decimal places allowed -")
                    continue
            if weight > 0:
                return weight
            else:
                print("- Invalid weight. Weight must be a positive number -")

        except ValueError:
            print("- Invalid input. Please enter a valid number-")

def checkStreetname():
    while True:
        print("Only letters and less then 100 characters")
        x = input("Enter Street name: ")
        if len(x) >= 1 and len(x) <= 100 and x.isalpha():
            return x
        else:
            print("-Invalid street name-")

def checkHousenumber():
    while True:
        print("House number (Up to 4 digits, optionally followed by 1 letter)")
        x = input("Enter house number: ")
        
        if re.match(r'^\d{1,4}[a-zA-Z]?$' , x):
            return x
        else:
            print("- Invalid house number. Please enter up to 4 digits, optionally followed by 1 letter -")

def checkZipcode():
    while True:
        print("Zipcode (4 digits, by 2 letter)")
        x = input("Enter zipcode: ")
        
        if re.match(r'^\d{4}[A-Za-z]{2}$' , x):
            return x
        else:
            print("- Invalid zipcode, (1234XX)-")

def checkCity():
    while True:
        print("Can only enter the following city's")
        cities = ['Rotterdam', 'Den Haag', 'Amsterdam', 'Schiedam', 'Leiden', 'Utrecht', 'Amersfoort', 'Groningen', 'Overijsel', 'Dordrecht']
        i = 0
        for x in cities:
            print(f'{i} - {x}')
            i = i + 1

        x = input("Enter a city: ")
        if x in cities:
            return x
        
def checkEmail():
    while True:
        print("email (example@example.com)")
        x = input("Enter email: ")
        
        if re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", x):
            return x
        else:
            print("- Invalid email-")

def checkMobile():
    while True:
        print("email (example@example.com)")
        x = "+31-6-" + input("Enter Mobile Phone: +31-6-")
        if re.match(r"^\+31-6-\d{8}$", x):
            return x
        else:
            print("-Invalid phone number-")
            
def checkIfUsernameExists(username):
    conn = connect_db()
    cursor = conn.cursor()
    # cursor.execute("SELECT username FROM Users WHERE username = ?", (username,))
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    conn.close()
    decrypted_users = []
    for user in users:
        decrypted_user = {
            'username': decrypt_message(user[1]),
        }
        decrypted_users.append(decrypted_user)
    filtered_users = [
        user for user in decrypted_users
        if username.lower() in user['username'].lower()
    ]
    if len(filtered_users) == 0:
        return False
    user = filtered_users[0]
    return user