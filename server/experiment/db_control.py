import sqlite3 as sq3


# Establish a connection to the SQLite database
def create_connection():
    conn = sq3.connect('password.db')
    return conn


# Create the users table
def create_table():
    print('running create_table')
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """)
        conn.commit()
        print('Table created successfully')
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()


# Add a new user to the database with an already hashed password
def add_user(username, hashed_password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO users (username, password)
    VALUES (?, ?)
    """, (username, hashed_password))
    conn.commit()
    conn.close()


# Remove a current user from the database
def remove_user():
    pass


# Check if a given username exists and if the password matches
def get_password(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result is None:
        return None

    else:
        stored_password_hash = result[0]

    return result[0] if result else None


# Get userid from database
def get_userid(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result is None:
        return None

    return result[0]


# Used for creating database
if __name__ == '__main__':
    create_table()
