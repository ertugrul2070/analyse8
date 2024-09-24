from db import connect_db, hashString
from logging import decrypt_message, encrypt_message
import hashlib

def get_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE user_type IN ('Consultant', 'Admin', 'Super')")
    users = cursor.fetchall()
    conn.close()

    decrypted_users = []
    for user in users:
        decrypted_user = {
            'user_id': user[0],
            'username': decrypt_message(user[1]),
            'password': user[2],
            'user_type': user[3],
        }
        decrypted_users.append(decrypted_user)

    filtered_users = [
        user for user in decrypted_users
        if username.lower() == user['username'].lower()
    ]
    
    if len(filtered_users) == 0:
        return None
    user = filtered_users[0]

    if user:
        user_id = user['user_id']
        username = user['username']
        stored_password = user['password']
        user_type = user['user_type']
        if verify_password(password, stored_password):
            return (user_id, user_type, username, password)
    return None

def verify_password(password, stored_password):
    return stored_password == hashlib.sha256(password.encode()).hexdigest()



def reinstatiateDB():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.executescript('''
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username BLOB NOT NULL UNIQUE,
    password TEXT NOT NULL,
    user_type TEXT NOT NULL CHECK (user_type IN ('Member', 'Consultant', 'Admin', 'Super'))
);

CREATE TABLE IF NOT EXISTS Members (
    uid INTEGER PRIMARY KEY AUTOINCREMENT,
    membership_id TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL CHECK (gender IN ('Male', 'Female')),
    weight REAL NOT NULL,
    street_name BLOB NOT NULL,
    house_number BLOB NOT NULL,
    zip_code BLOB NOT NULL,
    city BLOB NOT NULL,
    email_address BLOB NOT NULL,
    mobile_phone BLOB NOT NULL,
    registration_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users (user_id)
);

CREATE TABLE IF NOT EXISTS Profiles (
    consultant_admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users (user_id)
);
                   ''')
    conn.commit()
    conn.close()
    add_superadmin()

def add_superadmin():
    conn = connect_db()
    cursor = conn.cursor()
    # Check if SuperAdmin already exists
    cursor.execute("SELECT COUNT(*) FROM Users WHERE user_type = 'Super'")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return
    # Hash the password
    hashed_password = hashlib.sha256("Admin_123?".encode()).hexdigest()
    encrypted_username = encrypt_message('super_admin')
    # Insert SuperAdmin into the database
    cursor.execute("INSERT INTO Users (username, password, user_type) VALUES (?, ?, 'Super')",
                   (encrypted_username, hashed_password))
    conn.commit()
    conn.close()
