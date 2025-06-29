from datetime import datetime


class Invoice:
    """
    Clase que representa una factura en el sistema CRM.
    """

    def __init__(self, user_id, description, amount, status="pendiente", issue_date=None, id=None):
        self.id = id
        self.user_id = user_id
        self.description = description
        self.amount = amount
        self.status = status
        self.issue_date = issue_date or datetime.now()

    def __str__(self):
        return (
            f"ID: {self.id or 'Sin asignar'} | "
            f"Usuario ID: {self.user_id} | "
            f"Fecha: {self.issue_date.strftime('%d/%m/%Y')} | "
            f"Descripción: {self.description} | "
            f"Monto: {self.amount:.2f} € | "
            f"Estado: {self.status}"
        )
