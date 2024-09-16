from db import connect_db
from logging import decrypt_message
import re

def inputChecks(age, gender, weight, street_name, zip_code, city, email_address, mobile_phone, username, password):
    street_name = decrypt_message(street_name)
    zip_code = decrypt_message(zip_code)
    city = decrypt_message(city)
    email_address = decrypt_message(email_address)
    mobile_phone = decrypt_message(mobile_phone)
    username = decrypt_message(username)

    errors = []
    
    # Check gender
    if gender not in ["Male", "Female"]:
        errors.append("Gender should be 'Male' or 'Female'")
    
    # Check age
    try:
        age = int(age)
        if age <= 0:
            errors.append("Age should be a positive number")
    except ValueError:
        errors.append("Age should be a positive number")
    
    # Check weight
    try:
        weight = float(weight)
        if weight <= 0:
            errors.append("Invalid weight number")
    except ValueError:
        errors.append("Invalid weight number")
    
    # Check street name
    if not street_name.isalpha():
        errors.append("Street name should not include numbers or special characters")
    
    # Check zip code
    if not re.match(r"^\d{4}[A-Za-z]{2}$", zip_code):
        errors.append("Zip code should be for example: 1234AA")
    
    # Check city
    if not city.isalpha():
        errors.append("City should not include numbers or special characters")
    
    # Check email address
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email_address):
        errors.append("Email address should be for example: example@example.nl")
    
    # Check mobile phone
    if not re.match(r"^\+31-6-\d{8}$", mobile_phone):
        errors.append("Mobile phone should start with +31-6- and follow up with 8 numbers")

    # Check username
    if checkIfUsernameExists(username):
        errors.append("Username already exists.")
        
    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_'.]{7,9}$", username):
        errors.append("Username must have a length of at least 8 characters, no longer than 10 characters, start with a letter or underscore, and can contain letters, numbers, underscores, apostrophes, and periods.")
    
    # Check password
    if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_\-+=`|\(){}[\]:;\'<>,.?/]).{12,30}$', password):
        errors.append("Password must have a length of at least 12 characters and no longer than 30 characters, contain at least one lowercase letter, one uppercase letter, one digit, and one special character.")

    if errors:
        print("\n")
        print("Some fields have not been filled in correctly, ")
        for x in errors:
            print(f" - {x}")
        input("press ENTER to go back")
        return False
    else:
        return True
    
def editChecks(age, gender, weight, street_name, zip_code, city, email_address, mobile_phone):

    street_name = decrypt_message(street_name)
    zip_code = decrypt_message(zip_code)
    city = decrypt_message(city)
    email_address = decrypt_message(email_address)
    mobile_phone = decrypt_message(mobile_phone)

    errors = []
    
    # Check gender
    if gender not in ["Male", "Female"]:
        errors.append("Gender should be 'Male' or 'Female'")
    
    # Check age
    try:
        age = int(age)
        if age <= 0:
            errors.append("Age should be a positive number")
    except ValueError:
        errors.append("Age should be a positive number")
    
    # Check weight
    try:
        weight = float(weight)
        if weight <= 0:
            errors.append("Weight should be a positive number")
    except ValueError:
        errors.append("Weight should be a positive number")
    
    # Check street name
    if not street_name.isalpha():
        errors.append("Street name should not include numbers or special characters")
    
    # Check zip code
    if not re.match(r"^\d{4}[A-Za-z]{2}$", zip_code):
        errors.append("Zip code should be for example: 1234AA")
    
    # Check city
    if not city.isalpha():
        errors.append("City should not include numbers or special characters")
    
    # Check email address
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email_address):
        errors.append("Email address should be for example: example@example.nl")
    
    # Check mobile phone
    if not re.match(r"^\+31-6-\d{8}$", mobile_phone):
        errors.append("Mobile phone should start with +31-6- and follow up with 8 numbers")

    if errors:
        print("\n")
        print("Some fields have not been filled in correctly, ")
        for x in errors:
            print(f" - {x}")
        input("press ENTER to go back")
        return False
    else:
        return True
    
def inputConCheck(username, password):

    username = decrypt_message(username)

    errors = []

    # Check username
    if checkIfUsernameExists(username):
        errors.append("Username already exists.")

    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_'.]{7,9}$", username):
        errors.append("Username must have a length of at least 8 characters, no longer than 10 characters, start with a letter or underscore, and can contain letters, numbers, underscores, apostrophes, and periods.")
    
    # Check password
    if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_\-+=`|\(){}[\]:;\'<>,.?/]).{12,30}$', password):
        errors.append("Password must have a length of at least 12 characters and no longer than 30 characters, contain at least one lowercase letter, one uppercase letter, one digit, and one special character.")

    if errors:
        print("\n")
        print("Some fields have not been filled in correctly, ")

        for x in errors:
            print(f" - {x}")
        input("press ENTER to go back")
        return False
    else:
        return True

def checkPasswordReset(password):
    errors = []
    # Check password
    if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_\-+=`|\(){}[\]:;\'<>,.?/]).{12,30}$', password):
        errors.append("Password must have a length of at least 12 characters and no longer than 30 characters, contain at least one lowercase letter, one uppercase letter, one digit, and one special character.")

    if errors:
        print("\n")
        print("Some fields have not been filled in correctly, ")
        for x in errors:
            print(f" - {x}")
        input("press ENTER to go back")
        return False
    else:
        return True

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