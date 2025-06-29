# backend/repositories/invoice_repository.py

from backend.models.invoice import Invoice
from backend.utils.singleton import Singleton

class InvoiceRepository(metaclass=Singleton):
    """
    Repositorio para gestionar el almacenamiento de facturas en memoria.
    Implementado como Singleton para mantener consistencia de datos en el sistema.
    """

    def __init__(self):
        self.invoices = []

    def save_invoice(self, invoice: Invoice):
        self.invoices.append(invoice)

    def get_next_invoice_id(self):
        return f"INV{len(self.invoices) + 1:03d}"

    def find_by_user(self, user_email: str):
        # Busca por email, ya que el modelo usa `user_email`
        email = user_email.strip().lower()
        return [factura for factura in self.invoices if factura.user_email == email]

    def resumen_financiero_por_usuario(self, user_email: str):
        facturas = self.find_by_user(user_email)
        total_monto = sum(f.amount for f in facturas)
        pagadas = sum(f.amount for f in facturas if f.status_code == "2")
        pendientes = sum(f.amount for f in facturas if f.status_code == "1")
        canceladas = sum(f.amount for f in facturas if f.status_code == "3")

        return len(facturas), total_monto, pagadas, pendientes
