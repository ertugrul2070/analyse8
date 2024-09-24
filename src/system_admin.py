from db import connect_db, hashString
from datetime import date
from random import randint
from logging import encrypt_message, decrypt_message
from Checks2 import *

def get_search_members():
    print("The search function accepts the following keys (also partial): member ID, first name, last name, address, email address, and phone number")
    search_key = input("Enter here the key:")
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Members")
    encrypted_members = cursor.fetchall()
    conn.close()

    decrypted_members = []
    for member in encrypted_members:
        decrypted_member = {
            'uid': member[0],
            'membership_id': member[1],
            'user_id': member[2],
            'first_name': member[3],
            'last_name': member[4],
            'age': member[5],
            'gender': member[6],
            'weight': member[7],
            'street_name': decrypt_message(member[8]),
            'house_number': decrypt_message(member[9]),
            'zip_code': decrypt_message(member[10]),
            'city': decrypt_message(member[11]),
            'email_address': decrypt_message(member[12]),
            'mobile_phone': decrypt_message(member[13]),
            'registration_date': member[14],
        }
        decrypted_members.append(decrypted_member)

    filtered_members = [
        member for member in decrypted_members
        if search_key.lower() in member['membership_id'].lower() or
           search_key.lower() in member['first_name'].lower() or
           search_key.lower() in member['last_name'].lower() or
           search_key.lower() in member['street_name'].lower() or
           search_key.lower() in member['house_number'].lower() or
           search_key.lower() in member['zip_code'].lower() or
           search_key.lower() in member['city'].lower() or
           search_key.lower() in member['email_address'].lower() or
           search_key.lower() in member['mobile_phone'].lower()
    ]
    return filtered_members

def search_members():
    members = get_search_members()
    if members:
        print("\n")
        print("{:30s}".format("user_id, membership_id, first_name, last_name, age, gender, weight, street_name, house_number, zip_code, city, email_address, mobile_phone, registration_date"))
        print("#########################################################################################################################################################")
        for member in members:
            print("{:30s}".format(f"{member['user_id']} | {member['membership_id']} | {member['first_name']} | {member['last_name']} | {member['age']} | {member['gender']} | {member['weight']} | {member['street_name']} | {member['house_number']} | {member['zip_code']} | {member['city']} | {member['email_address']} | {member['mobile_phone']} | {member['registration_date']}"))
            print("---------------------------------------------------------------------------------------------------------------------------------")
    else:
        print("No members found.")
    input("press ENTER to go back")

def get_all_users():
    conn = connect_db()
    cursor = conn.cursor()
    # cursor.execute("SELECT * FROM Members JOIN Users on Members.user_id=Users.user_id")
    cursor.execute(""" SELECT 
    Users.user_id,
    COALESCE(Members.first_name, Profiles.first_name) AS first_name,
    COALESCE(Members.last_name, Profiles.last_name) AS last_name,
    Users.user_type
FROM 
    Users 
LEFT JOIN 
    Members ON Users.user_id = Members.user_id
LEFT JOIN 
    Profiles ON Users.user_id = Profiles.user_id
WHERE Users.user_type is not 'Super'
""")
    members = cursor.fetchall()
    conn.close()
    return members

def view_all_users():
    print("\nAll Users")
    members = get_all_users()
    if members:
        print("{:30s}".format(f"user_id, first_name, last_name, user_type"))
        print("##########################################")
        for member in members:
            print("{:30s}".format(f"{member[0]} | {member[1]} | {member[2]} | {member[3]}"))
            print("------------------------------------------")
    else:
        print("No users found.")
    input("press ENTER to go back")

def add_consultant_menu():
    print("\nAdd consultant | Leaving one of the fields empty will cancel the process")
    first_name = checkFirstName()
    last_name = checkLastName()
    username =  checkUserName()
    password = checkPassword()
    try:
        password = hashString(password)
        enc_username = encrypt_message(username)
        add_consultant(enc_username, password, first_name, last_name)
        print("Consultant added successfully.")
        return True, username
    except Exception as e:
        input("press ENTER to go back")
        return  False, ""

def add_consultant(username, password, first_name, last_name):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Users (username, password, user_type) VALUES (?, ?, 'Consultant')", (username, password))
        user_id = cursor.lastrowid
        cursor.execute("INSERT INTO Profiles (user_id, first_name, last_name) VALUES (? , ? , ?)", (user_id, first_name, last_name))
        conn.commit()
        conn.close()
    except:
        input("Something went wrong. Please press ENTER and try again..")

def getConsultantByUid(uid, typeToChoose):
    conn = connect_db()
    cursor = conn.cursor()
    # cursor.execute("SELECT * FROM Members JOIN Users on Members.user_id=Users.user_id")
    if typeToChoose == "Consultant":
        cursor.execute(f"SELECT * FROM Profiles JOIN Users on Profiles.user_id = Users.user_id WHERE Profiles.user_id = ?", (uid,))
    elif typeToChoose == "Member":
        cursor.execute(f"SELECT * FROM Members JOIN Users on Members.user_id = Users.user_id WHERE Members.user_id = ?", (uid,))
    member = cursor.fetchall()
    conn.close()
    return member

def edit_consultant_menu():
    uid = input("Enter the user_id of the consultant you want to edit: ")
    try:
        member = getConsultantByUid(uid, "Consultant")
    except:
        return False, ""
    if member:
        pass
    else:
        print(f"Consultant with user_id {uid} does not exist")
        input("press ENTER to go back")
        return False, ""
    member = member[0]
    print(f"\n\n###########################################################")
    print(f"Editing consultant")
    print(f"-> user_id: {uid}")
    print(f"-> firstname: {member[2]}")
    print(f"-> lastname: {member[3]}\n")
    first_name = checkFirstName()
    last_name = checkLastName()
    
    try:
        editConsultant(first_name, last_name, uid)
        print("Successfully edited consultant")
        input("press ENTER to go back")
        return True, decrypt_message(member[5])
    except Exception as e:
        print(e)
        print("something went wrong...")
        input("press ENTER to go back")
    return  False, ""


def editConsultant(first_name, last_name, uid):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"""
    UPDATE Profiles
    SET
        first_name = ?,
        last_name = ?
    WHERE
        user_id = {uid}
    """, (first_name, last_name))
    conn.commit()
    conn.close()

def deleteUser(uid, typeToRemove):
    conn = connect_db()
    cursor = conn.cursor()
    # cursor.execute("SELECT * FROM Members JOIN Users on Members.user_id=Users.user_id")
    if typeToRemove == "Consultant": 
        cursor.execute(f"DELETE FROM Profiles WHERE user_id = ?", (uid,))
    elif typeToRemove == "Member":
        cursor.execute(f"DELETE FROM Members WHERE user_id = ?", (uid,))
    conn.commit()
    cursor.execute(f"DELETE FROM Users WHERE user_id = ?", (uid,))
    conn.commit()
    conn.close()

def deleteMember(typeToRemove):
    if typeToRemove == "Member":
        uid = input("Enter the user_id of the member you want to delete: ")
    else:
        return False, ""
    try:
        member = getConsultantByUid(uid, typeToRemove)
    except:
        return False, ""
    if member:
        member = member[0]
        if (input(f"Are you sure you want to delete: {member[3]} {member[4]} (y/n)") == "y"):
            deleteUser(uid, typeToRemove)
            print("Succesfully deleted")
            input("press ENTER to go back")
            return True, decrypt_message(member[16])
        else:
            print("Consultant has NOT been deleted")
            input("press ENTER to go back")
            return  False, ""
    else:
        print(f"Consultant with user_id {uid} does not exist")
        input("press ENTER to go back")
        return  False, ""
    
def deleteConsultant_menu(typeToRemove):
    if typeToRemove == "Consultant":
        uid = input("Enter the user_id of the consultant you want to delete: ")
    elif typeToRemove == "Member":
        uid = input("Enter the user_id of the member you want to delete: ")
    else:
        return False, ""
    try:
        member = getConsultantByUid(uid, typeToRemove)
    except:
        return False, ""
    if member:
        member = member[0]
        if (input(f"Are you sure you want to delete: {member[2]} {member[3]} (y/n)") == "y"):
            deleteUser(uid, typeToRemove)
            print("Succesfully deleted")
            input("press ENTER to go back")
            return True, decrypt_message(member[5])
        else:
            print("Consultant has NOT been deleted")
            input("press ENTER to go back")
            return  False, ""
    else:
        print(f"Consultant with user_id {uid} does not exist")
        input("press ENTER to go back")
        return  False, ""
    
def resetPassword(uid = "", own = False):
    username = ""
    try:
        if own == False:
            uid = input("Enter the user_id of the consultant you want to reset the password of: ")
            if uid == "":
                return False, ""
            try:
                member = getConsultantByUid(uid, "Consultant")
            except:
                return False, ""
            if (member == []):
                print("Consultant does not exist")
                input("press ENTER to go back")
                return False, ""
            else:
                username = decrypt_message(member[0][5])
        print(f"rest password of: {username}")
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
        print(f"Password of {username} has been reset")
        input("press ENTER to go back")
        return True, username
    except Exception as e:
        return  False, ""