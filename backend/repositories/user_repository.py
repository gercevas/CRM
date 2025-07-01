import sqlite3
from backend.models.user import User
from backend.utils.singleton import Singleton
from backend.storage.database import get_connection
from datetime import datetime

class UserRepository(metaclass=Singleton):
    """
    Repositorio que gestiona el almacenamiento y recuperación de usuarios desde SQLite.
    """

    def save_user(self, user: User):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (id, first_name, last_name, email, phone, address, registration_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user.id,
            user.first_name,
            user.last_name,
            user.email,
            user.phone,
            user.address,
            user.registration_date or datetime.now().strftime("%Y-%m-%d")
        ))
        conn.commit()
        conn.close()

    def find_by_email(self, email: str):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE LOWER(email) = LOWER(?)", (email.strip(),))
        row = cursor.fetchone()
        conn.close()
        if row:
            return User(*row)
        return None

    def find_by_name(self, name: str):
        conn = get_connection()
        cursor = conn.cursor()
        name_like = f"%{name.strip().lower()}%"
        cursor.execute("""
            SELECT * FROM users 
            WHERE LOWER(first_name) LIKE ? OR LOWER(last_name) LIKE ?
        """, (name_like, name_like))
        rows = cursor.fetchall()
        conn.close()
        return [User(*row) for row in rows]

    def list_users(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        conn.close()
        return [User(*row) for row in rows]

    def get_next_user_id(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE id LIKE 'USR%'")
        rows = cursor.fetchall()
        conn.close()
        if not rows:
            return "USR001"
        numbers = [int(row[0].replace("USR", "")) for row in rows]
        next_num = max(numbers) + 1
        return f"USR{next_num:03}"
