from db import connect_db, hashString
from datetime import date
from random import randint
from logging import encrypt_message, decrypt_message
from Checks2 import *

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
    print("\nAdd Member | Leaving one of the fields empty will cancel the process")
    try:
        first_name = checkFirstName()
        last_name = checkLastName()
        age = checkAge()
        gender = checkGender()
        weight = checkWeight()
        street_name = encrypt_message(checkStreetname())
        house_number = encrypt_message(checkHousenumber())
        zip_code = encrypt_message(checkZipcode())
        city = encrypt_message(checkCity())
        email_address = encrypt_message(checkEmail())
        mobile_phone = encrypt_message(checkMobile())
        registration_date = date.today()
        username =  encrypt_message(checkUserName())
        password = checkPassword()
        membershipID = generateMembershipID()

        password = hashString(password)
        weight = float(weight)
        weight = int(weight * 100) / 100.0
        add_member(membershipID, username, password, first_name, last_name, age, gender, weight, street_name, house_number, zip_code, city, email_address, mobile_phone, registration_date)
        print("Member added successfully.")
        input("press ENTER to go back")
        return True, decrypt_message(username)
    except:
        input("press ENTER to go back")
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
    print(f"###########################################################\n")
    print(f"Editing member ID: {uid}")
    print(f"Firstname: {member[7]}")
    print(f"Lastname: {member[8]}")
    print(f"Age: {member[9]}")
    print(f"Gender: {member[10]}")
    print(f"Weight: {member[11]}")
    print(f"Streetname: {decrypt_message(member[12])}")
    print(f"Housenumber: {decrypt_message(member[13])}")
    print(f"Zipcode: {decrypt_message(member[14])}")
    print(f"City: {decrypt_message(member[15])}")
    print(f"Email: {decrypt_message(member[16])}")
    print(f"Mobilephone: {decrypt_message(member[17])}\n\n")    
    try:
        first_name = checkFirstName()
        last_name = checkLastName()
        age = checkAge()
        gender = checkGender()
        weight = checkWeight()
        street_name = encrypt_message(checkStreetname())
        house_number = encrypt_message(checkHousenumber())
        zip_code = encrypt_message(checkZipcode())
        city = encrypt_message(checkCity())
        email_address = encrypt_message(checkEmail())
        mobile_phone = encrypt_message(checkMobile())
        
        weight = float(weight)
        weight = int(weight * 100) / 100.0
        editMember(first_name, last_name, age, gender, weight, street_name, house_number, zip_code, city, email_address, mobile_phone, uid)
        print("Successfully edited member")
        input("press ENTER to go back")
        return True, decrypt_message(member[1])
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
        password = checkPassword()
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