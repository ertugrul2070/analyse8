import os
import datetime
from db import generate_and_save_key, load_key
from cryptography.fernet import Fernet

# Generate the key if it doesn't exist, otherwise load it
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, 'UniqueMeal.db')
if not os.path.exists(db_path):
    key = generate_and_save_key(Fernet.generate_key())
else:
    key = load_key()

cipher_suite = Fernet(key)

# Function to encrypt log messages
def encrypt_message(message):
    return cipher_suite.encrypt(message.encode())

# Function to decrypt log messages
def decrypt_message(encrypted_message):
    if encrypt_message != "":
        return cipher_suite.decrypt(encrypted_message).decode()
    else:
        return

# Function to log an activity
def log_activity(username, description, additional_info, suspicious=False):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_file_path = os.path.join(script_dir, 'encrypted_logs.log')

    if os.path.exists(log_file_path):
        with open(log_file_path, 'rb') as log_file:
            log_entry_no = sum(1 for _ in log_file) + 1
    else:
        log_entry_no = 1

    now = datetime.datetime.now()
    log_message = f"No: {log_entry_no}, Date: {now.strftime('%Y-%m-%d')}, Time: {now.strftime('%H:%M:%S')}, Username: {username}, Description: {description}, Additional Information: {additional_info}, Suspicious: {suspicious}"
    encrypted_message = encrypt_message(log_message)

    with open(log_file_path, 'ab') as log_file:
        log_file.write(encrypted_message + b'\n')

# Function to read and decrypt logs
def read_logs():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_file_path = os.path.join(script_dir, 'encrypted_logs.log')
    if os.path.exists(log_file_path):
        with open(log_file_path, 'rb') as log_file:
            for line in log_file:
                decrypted_message = decrypt_message(line.strip())
                print(decrypted_message)
    else:
        print("No logs found.")

# # Example usage
# log_activity('user1', 'Logged in', 'User logged in successfully', False)
# log_activity('user2', 'Failed login attempt', 'Incorrect password', True)

# # Example of reading and decrypting logs
# read_logs()
