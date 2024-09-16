from db import connect_db, hashString
from datetime import date
from random import randint
from logging import encrypt_message, decrypt_message
from Checks import inputChecks, editChecks, checkPasswordReset

def get_all_members():
    conn = connect_db()
    cursor = conn.cursor()
    # cursor.execute("SELECT * FROM Members JOIN Users on Members.user_id=Users.user_id")
    cursor.execute("SELECT * FROM Members JOIN Users on Members.user_id = Users.user_id")
    members = cursor.fetchall()
    conn.close()
    return members

def view_all_members():
    print("\nAll Members")
    members = get_all_members()
    if members:
        print("{:30s}".format("user_id, membership_id user_id, first_name last_name, age gender, weight street_name, house_number zip_code, city email_address, mobile_phone, registration_date"))
        print("#########################################################################################################################################################")
        for member in members:
            print("{:30s}".format(f"{member[15]} | {member[1]} {member[2]} | {member[3]} {member[4]} | {member[5]} {member[6]} | {member[7]} | {decrypt_message(member[8])} | {decrypt_message(member[9])} | {decrypt_message(member[10])} | {decrypt_message(member[11])} | {decrypt_message(member[12])} | {decrypt_message(member[13])} | {member[14]}"))
            print("---------------------------------------------------------------------------------------------------------------------------------")
    else:
        print("No members found.")
    input("press ENTER to go back")

def add_member_menu():
    cities = ['Rotterdam',  'Denhaag', 'Amsterdam', 'Schiedam', 'Leiden',  'Utrecht', 'Amersfoort', 'Groningen', 'Overijsel', 'Dordrecht']
    print("\nAdd Member | Leaving one of the fields empty will cancel the process")
    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    age = input("Enter Age: ")
    gender = input("Enter Gender (Male / Female): ")
    weight = input("Enter Weight (Use dot and max 2 numbers after decimal): ")
    street_name = encrypt_message(input("Enter Street Name: "))
    house_number = encrypt_message(input("Enter House Number: "))
    zip_code = encrypt_message(input("Enter Zip Code: "))
    i = 0
    for x in cities:
        print(f'{i} - {x}')
        i = i + 1
    try:
        citySelection = int(input("Choose your city by number: "))
        if citySelection < 0 or citySelection > 9:
            print("Invalid city selected, canceling the process")
            input("press Enter to continue: ")
            return False, ""
    except:
        print("No city selected, canceling the process")
        input("press Enter to continue: ")
        return False, ""
    city = encrypt_message(cities[citySelection])
    email_address = encrypt_message(input("Enter Email Address: "))
    mobile_phone = encrypt_message("+31-6-" + input("Enter Mobile Phone: +31-6-"))
    registration_date = date.today()
    print(" - Min 8 and max 10 characters long. Can start with `_` and can contain numbers, underscores, apostrophes, and periods")
    username =  encrypt_message(input("Enter Username: "))
    print(" - Min 12 and max 30 characters. contain at least one lowercase letter, one uppercase letter, one digit, and one special character")
    password = input("Enter password: ")
    membershipID = generateMembershipID()

    if not all([membershipID, username, password, first_name, last_name, age, gender, weight, street_name, house_number, zip_code, city, email_address, mobile_phone, registration_date]):
        print("Memeber has not been added")
        input("press ENTER to go back")
    else:
        # try:
        b = inputChecks(age, gender, weight, street_name, zip_code, city, email_address, mobile_phone, username, password)
        if b:
            password = hashString(password)
            weight = float(weight)
            weight = int(weight * 100) / 100.0
            add_member(membershipID, username, password, first_name, last_name, age, gender, weight, street_name, house_number, zip_code, city, email_address, mobile_phone, registration_date)
            print("Member added successfully.")
        else:
            return False, ""
        input("press ENTER to go back")
        return True, decrypt_message(username)
        # except Exception as e:
        #     print(e)
        #     input("press ENTER to go back")
    return False, ""
def add_member(membershipID, username, password, first_name, last_name, age, gender, weight, street_name, house_number, zip_code, city, email_address, mobile_phone, registration_date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users (username, password, user_type) VALUES (?, ?, 'Member')", (username, password))
    user_id = cursor.lastrowid
    cursor.execute("INSERT INTO Members (membership_id, user_id, first_name, last_name, age, gender, weight, street_name, house_number, zip_code, city, email_address, mobile_phone, registration_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_DATE)",
                   (membershipID, user_id, first_name, last_name, age, gender, weight, street_name, house_number, zip_code, city, email_address, mobile_phone))
    conn.commit()
    conn.close()

def generateMembershipID():
    today = str(date.today().year)[2:] #gets last 2 digits of current year
    basestring = today
    randstring = str(randint(0000000, 9999999))
    f = basestring + randstring
    total = 0
    for x in f:
        total += int(x)
    finalID = f + str(total % 10)
    return finalID

def checkMembershipID(id):
    year = str(date.today().year)[2:]
    if len(id) == 10:
        if int(id[:2]) <= year:
            midpart = id[2:(len(id) - 1)]
            lastpart = id[-1]
            total = 0
            for x in midpart:
                total = total + int(x)
            if lastpart == str(total % 10):
                return True
    return False

def getMemberByUid(uid):
    conn = connect_db()
    cursor = conn.cursor()
    # cursor.execute("SELECT * FROM Members JOIN Users on Members.user_id=Users.user_id")
    cursor.execute(f"SELECT * FROM Users LEFT JOIN Members ON Users.user_id =  Members.user_id WHERE Users.user_id = ? AND Users.user_type = 'Member'", (uid,))
    member = cursor.fetchall()
    conn.close()
    return member

def editMemberMenu():
    uid = input("Enter the user_id of the member you want to edit: ")
    if uid:
        try:
            member = getMemberByUid(uid)
            if member == []:
                return False, ""
        except:
            return False, ""
    else:
        print("Member not found")
        input("press ENTER to go back")
        return False, ""
    member = member[0]
    print(f"###########################################################")
    print(f"Editing member {uid} {member[7]} {member[8]}")
    print(f"Leave the field empty if you do not want to change it")
    print(f"\nOriginal | Change into...")
    
    try:
        cities = ['Rotterdam',  'Denhaag', 'Amsterdam', 'Schiedam', 'Leiden',  'Utrecht', 'Amersfoort', 'Groningen', 'Overijsel', 'Dordrecht']
        first_name = input("Firstname " + member[7] + ": ") or member[7]
        last_name = input("Lastname " +member[8] + ": ") or member[8]
        age = input("Age " +str(member[9]) + ": ") or member[9]
        gender = input("Gender " + member[10] + ": ") or member[10]
        weight = input("Weight " +str(member[11]) + ": ") or member[11]
        street_name = encrypt_message(input("Streetname " + decrypt_message(member[12]) + ": ") or decrypt_message(member[12]))
        house_number = encrypt_message(input("Housenumber " +decrypt_message(member[13]) + ": ") or decrypt_message(member[13]))
        zip_code = encrypt_message(input("Zipcode " + decrypt_message(member[14]) + ": ") or decrypt_message(member[14]))
        city = member[15]
        i = 0
        for x in cities:
            print(f'{i} - {x}')
            i = i + 1
        try:
            citySelection = input("Choose your city by number: ")
            if citySelection != "":
                citySelection = int(citySelection)
                if citySelection > 0 or citySelection < 9:
                    city = encrypt_message(cities[citySelection])
                else:
                    print("Invalid city selected, canceling the process")
                    input("press Enter to continue: ")
                    return False, ""
        except:
            print("No city selected, canceling the process")
            input("press Enter to continue: ")
            return False, ""
        
        email_address = encrypt_message(input("Emailadress " + decrypt_message(member[16]) + ": ") or decrypt_message(member[16]))
        
        mobile_phone_input = input("Mobilephone " + decrypt_message(member[17]) + ": +31-6-")
        mobile_phone = decrypt_message(member[17]) if mobile_phone_input == "" else "+31-6-" + mobile_phone_input
        mobile_phone = encrypt_message(mobile_phone)
        
        if  editChecks(age, gender, weight, street_name, zip_code, city, email_address, mobile_phone):
            weight = float(weight)
            weight = int(weight * 100) / 100.0
            editMember(first_name, last_name, age, gender, weight, street_name, house_number, zip_code, city, email_address, mobile_phone, uid)
            print("Successfully edited member")
            input("press ENTER to go back")
            return True, decrypt_message(member[1])
        else:
            return False, ""
    except Exception as e:
        input("press ENTER to go back")
        return False, ""

def editMember(first_name, last_name, age, gender, weight, street_name, house_number, zip_code, city, email_address, mobile_phone, uid):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"""
    UPDATE Members
    SET
        first_name = ?,
        last_name = ?,
        age = ?,
        gender = ?,
        weight = ?,
        street_name = ?,
        house_number = ?,
        zip_code = ?,
        city = ?,
        email_address = ?,
        mobile_phone = ?
    WHERE
        user_id = {uid}
    """, (first_name, last_name, age, gender, weight, street_name, house_number, zip_code, city, email_address, mobile_phone))
    conn.commit()
    conn.close()

def resetConPassword(uid = ""):
    username = ""
    try:
        print("leaving the password field empty will set cancel the password change")
        password = input("Enter the new password: ")
        if checkPasswordReset(password) == False:
            return False, ""
        if len(password) == 0:
            return False, ""
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(f"""
        UPDATE Users
        SET password = ?
        WHERE user_id = ?
        """, (hashString(password), int(uid)))
        conn.commit()
        conn.close()
        print(f"Password of {uid} has been reset")
        input("press ENTER to go back")
        return True, decrypt_message(username)
    except Exception as e:
        return  False, ""