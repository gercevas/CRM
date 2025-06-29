from backend.models.invoice import Invoice
from backend.storage.database import get_connection


class InvoiceRepository:
    """
    Repositorio para manejar operaciones con la tabla de facturas.
    """

    def __init__(self):
        self.conn = get_connection()
        self._create_table()

    def _create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                status TEXT NOT NULL,
                issue_date TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        self.conn.commit()

    def save_invoice(self, invoice: Invoice):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO invoices (id, user_id, description, amount, status, issue_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            invoice.id,
            invoice.user_id,
            invoice.description,
            invoice.amount,
            invoice.status,
            invoice.issue_date.strftime("%Y-%m-%d %H:%M:%S")
        ))
        self.conn.commit()

    def find_by_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM invoices WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        return [Invoice(*row) for row in rows]

    def get_next_invoice_id(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM invoices ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        if not row:
            return "FAC001"
        last_id = int(row[0].replace("FAC", ""))
        return f"FAC{last_id + 1:03}"

    def resumen_financiero_por_usuario(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT
                COUNT(*) as total_facturas,
                SUM(amount) as monto_total,
                SUM(CASE WHEN status = 'pagado' THEN amount ELSE 0 END) as pagado,
                SUM(CASE WHEN status = 'pendiente' THEN amount ELSE 0 END) as pendiente
            FROM invoices
            WHERE user_id = ?
        """, (user_id,))
        return cursor.fetchone()
