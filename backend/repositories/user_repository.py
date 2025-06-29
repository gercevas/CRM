from backend.models.user import User
from backend.storage.database import get_connection

class UserRepository:
    """
    Clase que gestiona operaciones de base de datos relacionadas con usuarios.
    Esta clase es compatible con SQLite y PostgreSQL.
    """

    def __init__(self):
        self.conn = get_connection()
        self._create_table()

    def _create_table(self):
        """
        Crea la tabla de usuarios si no existe.
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT,
                address TEXT,
                registration_date TEXT
            )
        """)
        self.conn.commit()

    def save_user(self, user: User):
        cursor = self.conn.cursor()
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
            user.registration_date
        ))
        self.conn.commit()

    def find_by_email(self, email: str):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        return User(*row) if row else None

    def find_by_name(self, name: str):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM users
            WHERE first_name LIKE ? OR last_name LIKE ?
        """, (f"%{name}%", f"%{name}%"))
        rows = cursor.fetchall()
        return [User(*row) for row in rows]

    def list_all(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return [User(*row) for row in rows]
