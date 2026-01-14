import sqlite3

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Foydalanuvchilar jadvali: ID, username, balans va taklif qilgan odam IDsi
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            balance REAL DEFAULT 0.0,
            referrer_id INTEGER DEFAULT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_user(user_id, username, referrer_id=None):
    """Foydalanuvchini bazaga qo'shish (3 ta argument bilan)"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Agar foydalanuvchi allaqachon bo'lsa, INSERT OR IGNORE uni o'tkazib yuboradi
    cursor.execute(
        'INSERT OR IGNORE INTO users (user_id, username, referrer_id) VALUES (?, ?, ?)',
        (user_id, username, referrer_id)
    )
    conn.commit()
    conn.close()

def get_user_data(user_id):
    """Foydalanuvchining balansi va referal ma'lumotlarini olish"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT balance, referrer_id FROM users WHERE user_id = ?', (user_id,))
    res = cursor.fetchone()
    conn.close()
    return res # (balance, referrer_id) qaytaradi

def get_balance(user_id):
    """Faqat balansni qaytarish"""
    data = get_user_data(user_id)
    return data[0] if data else 0

def update_balance(user_id, amount):
    """Balansni to'ldirish (Admin tasdiqlaganda ishlatiladi)"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, user_id))
    conn.commit()
    conn.close()

def decrease_balance(user_id, amount):
    """Xizmat uchun balansdan pul yechish"""
    current_balance = get_balance(user_id)
    if current_balance >= amount:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (amount, user_id))
        conn.commit()
        conn.close()
        return True
    return False # Mablag' yetarli bo'lmasa False qaytaradi