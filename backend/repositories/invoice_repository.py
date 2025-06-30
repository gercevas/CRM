import sqlite3
from backend.models.invoice import Invoice
from backend.utils.singleton import Singleton
from backend.storage.database import get_connection
from datetime import datetime

class InvoiceRepository(metaclass=Singleton):
    """
    Repositorio para gestionar el almacenamiento de facturas en SQLite.
    """

    def save_invoice(self, invoice: Invoice):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO invoices (id, user_id, description, amount, status_code, issue_date, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            invoice.id,
            invoice.user_email,  # Aquí se usa el email como identificador, tal como has indicado
            invoice.description,
            invoice.amount,
            invoice.status_code,
            invoice.issue_date,
            invoice.created_at
        ))
        conn.commit()
        conn.close()

    def get_next_invoice_id(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM invoices WHERE id LIKE 'INV%'")
        rows = cursor.fetchall()
        conn.close()
        if not rows:
            return "INV001"
        numbers = [int(row[0].replace("INV", "")) for row in rows]
        next_num = max(numbers) + 1
        return f"INV{next_num:03}"

    def find_by_user(self, user_email: str):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM invoices WHERE LOWER(user_id) = LOWER(?)", (user_email.strip(),))
        rows = cursor.fetchall()
        conn.close()
        return [Invoice(*row) for row in rows]

    def resumen_financiero_por_usuario(self, user_email: str):
        facturas = self.find_by_user(user_email)
        total_monto = sum(f.amount for f in facturas)
        pagadas = sum(f.amount for f in facturas if f.status_code == "2")
        pendientes = sum(f.amount for f in facturas if f.status_code == "1")
        canceladas = sum(f.amount for f in facturas if f.status_code == "3")
        return len(facturas), total_monto, pagadas, pendientes
