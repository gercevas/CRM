import sqlite3
import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Ruta al archivo de base de datos
DB_PATH = os.getenv("SQLITE_PATH", "crm.sqlite")

def create_tables():
    # Conectar a SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Crear tabla de usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT,
        address TEXT,
        registration_date TEXT NOT NULL
    );
    """)

 # Crear tabla de facturas (alineada con el modelo Invoice)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoices (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        description TEXT NOT NULL,
        amount REAL NOT NULL,
        status_code TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    """)


    conn.commit()
    conn.close()
    print("Tablas creadas correctamente en crm.sqlite")

if __name__ == "__main__":
    create_tables()
