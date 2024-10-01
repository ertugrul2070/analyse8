from db import connect_db, hashString
from datetime import date
from random import randint
from logging import encrypt_message, decrypt_message
from Checks2 import *

def add_system_menu():
    print("\n* Add System:")
    try:
        first_name = checkFirstName()
        last_name = checkLastName()
        username =  encrypt_message(checkUserName())
        password = checkPassword()
        password = hashString(password)
        add_system(username, password, first_name, last_name)
        print("System admin added successfully.")
        input("press ENTER to go back")
        return True, decrypt_message(username)
    except Exception as e:
        input("press ENTER to go back")
        return  False, ""
        
def add_system(username, password, first_name, last_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users (username, password, user_type) VALUES (?, ?, 'Admin')", (username, password))
    user_id = cursor.lastrowid
    cursor.execute("INSERT INTO Profiles (user_id, first_name, last_name) VALUES (? , ? , ?)", (user_id, first_name, last_name))
    conn.commit()
    conn.close()

def getSystemByUid(uid):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Profiles JOIN Users on Profiles.user_id = Users.user_id WHERE Users.user_id = ? AND Users.user_type = 'Admin'", (uid,))
    member = cursor.fetchall()
    conn.close()
    return member

def edit_system_menu():
    print("\n* Edit system admin:")
    uid = input("Enter the user_id of the system admin you want to edit: ")
    member = getSystemByUid(uid)
    if member:
        member = member[0]
    else:
        print(f"System admin with user_id {uid} does not exist")
        input("press ENTER to go back")
        return False, ""
    
    print(f"\n\n###########################################################")
    print(f"* Editing system admin {uid}")
    print(f" -Firstname: {member[2]}")
    print(f" -Lastname: {member[3]}")
    print(f"Leave the field empty if you do not want to change it")
    print(f"\nOriginal | Change into...")
    
    first_name = checkFirstName()
    last_name = checkLastName()
    
    try:
        editSystemAdmin(first_name, last_name, uid)
        print("Successfully edited system admin")
        input("press ENTER to go back")
        return True, decrypt_message(member[5])
    except Exception as e:
        input("press ENTER to go back")
        return False, ""

def editSystemAdmin(first_name, last_name, uid):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"""
    UPDATE Profiles
    SET
        first_name = ?,
        last_name = ?
    WHERE
        user_id = ?
    """, (first_name, last_name, uid))
    conn.commit()
    conn.close()

def deleteUser(uid):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM Profiles WHERE user_id = {uid}")
    conn.commit()
    cursor.execute(f"DELETE FROM Users WHERE user_id = {uid}")
    conn.commit()
    conn.close()

def deleteSystemAdmin_menu():
    print("\n* Deleting System Admin:")
    uid = input("Enter the user_id of the system admin you want to delete: ")
    try:
        member = getSystemByUid(uid)
    except:
        return False, ""

    if member:
        member = member[0]
        if (input(f"Are you sure you want to delete: {member[2]} {member[3]} (y/n)") == "y"):
            deleteUser(uid)
            print("Succesfully deleted")
            input("press ENTER to go back")
            return True, decrypt_message(member[5])  
        else:
            print("System admin has NOT been deleted")
            input("press ENTER to go back")
            return False, ""
    else:
        print(f"System admin with user_id {uid} does not exist")
        input("press ENTER to go back")
        return False, ""
        
    
def systemResetPassword(uid = "", own = False):
    print("\n* Reset password:")
    try:
        username = ""
        if own == False:
            uid = input("Enter the user_id of the system admin you want to reset the password of: ")
            try:
                member = getSystemByUid(uid)
            except:
                return False, ""
            if (member == []):
                print("System admin does not exist")
                input("press ENTER to go back")
                return False, ""
            else:
                member = member[0]
                username = member[5]
        print("leaving the password field empty will cancel the password change")
        password = checkPassword()
        if password == None:
            input("Action cancelled, press ENTER to go back")
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