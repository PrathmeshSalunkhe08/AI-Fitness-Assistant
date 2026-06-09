import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

def connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="ai_fitness",
        port=3307
    )

# ---------- REGISTER ----------
def register_user(name, email, password):
    hashed = generate_password_hash(password)
    db = connection()
    cr = db.cursor()
    cr.execute(
        "INSERT INTO users(name,email,password) VALUES(%s,%s,%s)",
        (name, email, hashed)
    )
    db.commit()
    db.close()

# ---------- CHECK EMAIL ----------
def email_exists(email):
    db = connection()
    cr = db.cursor()
    cr.execute("SELECT id FROM users WHERE email=%s", (email,))
    result = cr.fetchone()
    db.close()
    return result

# ---------- LOGIN ----------
def login_user(email, password):
    db = connection()
    cr = db.cursor()
    cr.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cr.fetchone()
    db.close()

    if user and check_password_hash(user[3], password):
        return user
    return None




import datetime

def get_or_create_session(user_id):
    today = datetime.date.today()

    db = connection()
    cr = db.cursor()

    cr.execute("""
        SELECT id FROM chat_sessions 
        WHERE user_id=%s AND session_date=%s
    """, (user_id, today))

    result = cr.fetchone()

    if result:
        session_id = result[0]
    else:
        cr.execute("""
            INSERT INTO chat_sessions (user_id, session_date)
            VALUES (%s, %s)
        """, (user_id, today))
        db.commit()
        session_id = cr.lastrowid


    db.close()
    return session_id


def create_new_session(user_id):
    today = datetime.date.today()
    db = connection()
    cr = db.cursor()

    cr.execute("""
        INSERT INTO chat_sessions (user_id, session_date)
        VALUES (%s, %s)
    """, (user_id, today))
    
    db.commit()
    session_id = cr.lastrowid
    db.close()
    return session_id




def save_message(session_id, sender, message):
    db = connection()
    cr = db.cursor()

    cr.execute("""
        INSERT INTO chat_messages (session_id, sender, message)
        VALUES (%s, %s, %s)
    """, (session_id, sender, message))

    db.commit()
    db.close()




def get_user_sessions(user_id):
    db = connection()
    cr = db.cursor()

    cr.execute("""
        SELECT id, session_date
        FROM chat_sessions
        WHERE user_id=%s
        ORDER BY session_date DESC
    """, (user_id,))

    sessions = cr.fetchall()
    db.close()
    return sessions


def get_session_messages(session_id):
    db = connection()
    cr = db.cursor()

    cr.execute("""
        SELECT id, sender, message
        FROM chat_messages
        WHERE session_id=%s
        ORDER BY created_at
    """, (session_id,))

    messages = cr.fetchall()
    db.close()
    return messages


def delete_session(session_id):
    db = connection()
    cr = db.cursor()

    cr.execute("DELETE FROM chat_sessions WHERE id=%s", (session_id,))
    db.commit()
    db.close()


def delete_message(message_id):
    db = connection()
    cr = db.cursor()

    cr.execute("DELETE FROM chat_messages WHERE id=%s", (message_id,))
    db.commit()
    db.close()
