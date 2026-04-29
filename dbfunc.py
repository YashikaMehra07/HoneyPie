import sqlite3
from datetime import datetime

DATABASE= "HoneyPie0.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    return cursor, conn


def init_db(app):
    with app.app_context():
        cursor, conn = get_db_connection()
        # cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mood_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                mood1 TEXT NOT NULL,
                mood2 TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id) )
        ''')
        conn.commit()

# def add_user(username, password):
#     cursor, conn = get_db_connection()
#     cursor.execute('''
#     INSERT INTO users (username, password) VALUES (?, ?)
#     ''', (username, password))
#     conn.commit()
#     conn.close()

def get_user_bymail(email):
    cursor, conn= get_db_connection()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user= cursor.fetchone()  # since we using rowfactory it returns{'id': anyid452122}
    conn.close()
    return user


def get_user_byname(username):
    cursor, conn= get_db_connection()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user= cursor.fetchone()  # since we using rowfactory it returns{'id': anyid452122}
    conn.close()
    return user

def store_user_mood_data(username, mood1, mood2):
    cursor, conn = get_db_connection()
    user= get_user_byname(username)
    timestamp = datetime.now().isoformat()
    if not user:
        return False
    cursor.execute('''
    INSERT INTO mood_data (user_id, mood1, mood2, timestamp)
    VALUES (?, ?, ?, ?)
    ''', (user['id'], mood1, mood2, timestamp))
    conn.commit()
    conn.close()

def print_all_users():
    cursor, conn = get_db_connection()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    for user in users:
        print(dict(user))  # Assuming you're using row_factory
    conn.close()


def get_user_mood_data(username):
    cursor, conn = get_db_connection()
    user= get_user_byname(username)
    if user is None:
        return []
    cursor.execute('''
    SELECT timestamp, mood1, mood2 FROM mood_data WHERE user_id = ?
                   ORDER BY timestamp DESC
    ''', (user['id'],)) #since using rowfactory returns data in the form of dict
    data = cursor.fetchall()
    conn.close()
    # return data[0] if data else None
    return data if data else None

