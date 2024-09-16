from login  import get_user, reinstatiateDB
from consultant import add_member_menu, view_all_members, editMemberMenu, resetConPassword
from system_admin import *
from super_admin import *
from backup import create_backup, restore_backup
from logging import log_activity, read_logs
import getpass
import os

def login():
    reinstatiateDB()
    rememberUsername = ''
    countTries = 0
    while True:
        username = input("Username: ")
        password = getpass.getpass("Password: ")

        # username = "super_admin"
        # password = "Admin_123?"
        user = []
        if username != "" and password != "":
            user = get_user(username, password)
        
        if user:
            log_activity(username, 'Logged in', 'User logged in successfully', False)
            return user
        else:
            rememberUsername = username
            if rememberUsername == username:
                countTries = countTries + 1
            else:
                countTries = 0
            if countTries == 3:
                log_activity('', 'Unsuccessful login', f'Multiple unsuccessful tries in a row for {username}', True)
                return None
            log_activity('', 'Unsuccessful login', f'username: {username} is used for a login attempt with a wrong password', False)
            print("Invalid credentials.")

def consultant_menu(user_type, user_id, username):
    while True:
        print("-"*50)
        print(f"{user_type} Menu | Navigate by entering the number of your choice")
        print("1. View Members")
        print("2. Add a Member")
        print("3. Edit a Member")
        print("4. Reset your password")
        print("5. Search for a member")
        print("6. Log out")
        choice = input("Enter choice: ")
        if choice == '1':
            view_all_members()
        elif choice == '2':
            b, u = add_member_menu()
            if b:
                log_activity(username, 'New member is created', f'username: {u}', False)
        elif choice == '3':
            b, u = editMemberMenu()
            if b:
                log_activity(username, 'Member is edited', f'username: {u}', False)
        elif choice == "4":
            b, u  = resetConPassword(user_id)
            if b:
                log_activity(username, 'Consultant password is reset', f'username: {username}', False)
        elif choice == "5":
            search_members()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

def system_admin_menu(user_type, user_id, username):
    while True:
        print("-"*50)
        print(f"{user_type} Menu | Navigate by entering the number of your choice")
        print("1. Search members")
        print("2. View users")
        print("3. Add a consultant")
        print("4. Edit a consultant")
        print("5. Delete a consultant")
        print("6. Reset consultant password")
        print("7. See log files")
        print("8. Add new member")
        print("9. Edit a member")
        print("10. Delete a member")
        print("11. Change your password")
        print("12. System backup")
        print("13. Log out")
        choice = input("Enter choice: ")
        if choice == '1':
            search_members()
        elif choice == '2':
            view_all_users()
        elif choice == '3':
            b, u = add_consultant_menu()
            if b:
                log_activity(username, 'New consultant is created', f'username: {u}', False)
        elif choice == "4":
            b, u = edit_consultant_menu()
            if b:
                log_activity(username, 'Consultant is edited', f'username: {u}', False)
        elif choice == "5":
            b, u = deleteConsultant_menu("Consultant")
            if b:
                log_activity(username, 'Consultant is deleted', f'username: {u}', False)
        elif choice == "6":
            b, u = resetPassword()
            if b:
                log_activity(username, 'Consultant password is reset', f'username: {u}', False)
        elif choice == "7":
            read_logs()
        elif choice == "8":
            b, u = add_member_menu()
            if b:
                log_activity(username, 'Consultant password is reset', f'username: {u}', False)
        elif choice == "9":
            b, u = editMemberMenu()
            if b:
                log_activity(username, 'Member is edited', f'username: {u}', False)
        elif choice == "10":
            b, u = deleteMember("Member")
            if b:
                log_activity(username, 'Member is deleted', f'username: {u}', False)
        elif choice == "11":
            b, u  = resetPassword(user_id, True)
            if b:
                log_activity(username, 'Consultant password is reset', f'username: {username}', False)
        elif choice == "12":
            print("1. Make a system  backup")
            print("2. Load a system  backup")
            choise2 =  input("Enter choice: ")
            if choise2 == "1":
                b, u = create_backup()
                if b:
                    log_activity(username, 'Created backup of system', f'filename: {u}', False)
            elif choise2 == "2":
                b, u = restore_backup()
                if b:
                    log_activity(username, 'Loaded backup of system', f'filename: {u}', False)
            else:
                return
        elif choice == "13":
            break
        else:
            print("Invalid choice. Please try again.")

def super_admin_menu(user_type, user_id, username):
    while True:
        print("-"*50)
        print(f"{user_type} Menu | Navigate by entering the number of your choice")
        print("1. Search members")
        print("2. View users")
        print("3. Add a consultant")
        print("4. Edit a consultant")
        print("5. Delete a consultant")
        print("6. Reset consultant password")
        print("7. See log files")
        print("8. Add new member")
        print("9. Edit a member")
        print("10. Delete a member")
        print("11. Change my password")
        print("12. Add system admin")
        print("13. Edit system admin")
        print("14. Delete system admin")
        print("15. Change system admin password ")
        print("16. System backup ")
        print("17. Logout")
        choice = input("Enter choice: ")
        if choice == '1':
            search_members()
        elif choice == '2':
            view_all_users()
        elif choice == '3':
            b, u = add_consultant_menu()
            if b:
                log_activity(username, 'New consultant is created', f'username: {u}', False)
        elif choice == "4":
            b, u = edit_consultant_menu()
            if b:
                log_activity(username, 'Consultant is edited', f'username: {u}', False)
        elif choice == "5":
            b, u = deleteConsultant_menu("Consultant")
            if b:
                log_activity(username, 'Consultant is deleted', f'username: {u}', False)
        elif choice == "6":
            b, u = resetPassword()
            if b:
                log_activity(username, 'Consultant password is reset', f'username: {u}', False)
        elif choice == "7":
            read_logs()
            input("press ENTER to go back")
        elif choice == "8":
            b, u = add_member_menu()
            if b:
                log_activity(username, 'New member is created', f'username: {u}', False)
        elif choice == "9":
            b, u = editMemberMenu()
            if b:
                log_activity(username, 'Member is edited', f'username: {u}', False)
        elif choice == "10":
            b, u = deleteMember("Member")
            if b:
                log_activity(username, 'Member is deleted', f'username: {u}', False)
        elif choice == "11":
            b, u = systemResetPassword(user_id, True)
            if b:
                log_activity(username, 'Superadmin password changed', f'username: {username}', False)
        elif choice == "12":
            b, u = add_system_menu()
            if b:
                log_activity(username, 'New system admin created', f'username: {u}', False)
        elif choice == "13":
            b, u = edit_system_menu()
            if b:
                log_activity(username, 'system admin is edited', f'username: {u}', False)
        elif choice == "14":
            b, u = deleteSystemAdmin_menu()
            if b:
                log_activity(username, 'System admin is deleted', f'username: {u}', False)
        elif choice == "15":
            b, u = systemResetPassword()
            if b:
                log_activity(username, 'System admin password is reset', f'username: {u}', False)
        elif choice == "16":
            print("1. Make a system  backup")
            print("2. Load a system  backup")
            choise2 =  input("Enter choice: ")
            if choise2 == "1":
                b, u = create_backup()
                if b:
                    log_activity(username, 'Created backup of system', f'filename: {u}', False)
            elif choise2 == "2":
                b, u = restore_backup()
                if b:
                    log_activity(username, 'Loaded backup of system', f'filename: {u}', False)
        elif choice == "17":
            break
        else:
            print("Invalid choice. Please try again.")
def main():
    while True:
        print("Welcome to the UniqueMeal system")
        user = login()
        if user != None:
            user_id, user_type, username = user
            if user_type == 'Consultant':
                consultant_menu(user_type, user_id, username)
            elif user_type =='Admin':
                system_admin_menu(user_type, user_id, username)
            elif user_type == "Super":
                super_admin_menu(user_type, user_id, username)
        else:
            break

if __name__ == "__main__":
    main()
