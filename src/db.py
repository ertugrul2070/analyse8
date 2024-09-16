import sqlite3
import hashlib
import uuid
import os

def connect_db():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Define the database path in the same directory as the script
    db_path = os.path.join(script_dir, 'UniqueMeal.db')
    # Create or connect to the database
    connection = sqlite3.connect(db_path)
    return connection

# Function to generate and save the encryption key to a database
def generate_and_save_key(key):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS encryption_keys (id INTEGER PRIMARY KEY, key BLOB)''')
    cursor.execute('INSERT INTO encryption_keys (key) VALUES (?)', (key,))
    conn.commit()
    conn.close()
    return key


# Function to load the encryption key from the database
def load_key():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT key FROM encryption_keys ORDER BY id DESC LIMIT 1')
    key = cursor.fetchone()[0]
    conn.close()
    return key

def hashString(input):
    return hashlib.sha256(str(input).encode()).hexdigest()