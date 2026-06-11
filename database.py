# =============================================
#         AgroKhet AI - Database File
# =============================================

import sqlite3
import bcrypt
from config import DATABASE_NAME

# --- CONNECT TO DATABASE ---
def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# --- CREATE ALL TABLES ---
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            state TEXT,
            language TEXT DEFAULT 'English',
            profile_pic TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # SCAN HISTORY TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            image_path TEXT,
            disease_name TEXT,
            confidence TEXT,
            treatment TEXT,
            scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # MY FARM TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS my_farm (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            crop_name TEXT,
            land_size TEXT,
            sow_date TEXT,
            harvest_date TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # OTP TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS otp_store (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            otp TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database tables created successfully!")


# --- REGISTER NEW USER ---
def register_user(full_name, email, phone, password, state, language):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Hash password securely
        hashed = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        )
        cursor.execute('''
            INSERT INTO users 
            (full_name, email, phone, password, state, language)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (full_name, email, phone, hashed, state, language))
        conn.commit()
        return True, "✅ Registration successful!"
    except sqlite3.IntegrityError:
        return False, "❌ Email or Phone already exists!"
    finally:
        conn.close()


# --- LOGIN USER ---
def login_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM users WHERE email = ?', (email,)
    )
    user = cursor.fetchone()
    conn.close()
    if user:
        # Check password
        if bcrypt.checkpw(
            password.encode('utf-8'),
            user['password']
        ):
            return True, dict(user)
        else:
            return False, "❌ Wrong password!"
    return False, "❌ Email not found!"


# --- GET USER BY EMAIL ---
def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM users WHERE email = ?', (email,)
    )
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None


# --- UPDATE PASSWORD ---
def update_password(email, new_password):
    conn = get_connection()
    cursor = conn.cursor()
    hashed = bcrypt.hashpw(
        new_password.encode('utf-8'),
        bcrypt.gensalt()
    )
    cursor.execute(
        'UPDATE users SET password = ? WHERE email = ?',
        (hashed, email)
    )
    conn.commit()
    conn.close()
    return True, "✅ Password updated!"


# --- SAVE SCAN HISTORY ---
def save_scan(user_id, image_path, disease_name, confidence, treatment):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO scan_history
        (user_id, image_path, disease_name, confidence, treatment)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, image_path, disease_name, confidence, treatment))
    conn.commit()
    conn.close()


# --- GET SCAN HISTORY ---
def get_scan_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM scan_history
        WHERE user_id = ?
        ORDER BY scanned_at DESC
    ''', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


# --- SAVE FARM DATA ---
def save_farm(user_id, crop_name, land_size, sow_date, harvest_date, notes):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO my_farm
        (user_id, crop_name, land_size, sow_date, harvest_date, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, crop_name, land_size, sow_date, harvest_date, notes))
    conn.commit()
    conn.close()


# --- GET FARM DATA ---
def get_farm_data(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM my_farm
        WHERE user_id = ?
        ORDER BY created_at DESC
    ''', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


# --- INITIALIZE DATABASE ---
create_tables()