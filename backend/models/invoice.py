from datetime import datetime
class Invoice:
    """
    Clase que representa una factura asociada a un usuario del sistema CRM.
    """

    STATUS_OPTIONS = {
        "1": "Pendiente",
        "2": "Pagada",
        "3": "Cancelada"
    }

    def __init__(self, id, user_email, description, amount, status_code, created_at=None):
        self.id = id
        self.user_email = user_email.strip().lower()
        self.description = description.strip()
        self.amount = float(amount)
        self.status_code = status_code.strip()
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def status_text(self):
        return self.STATUS_OPTIONS.get(self.status_code, "desconocido")

    def to_dict(self):
        return {
            "id": self.id,
            "user_email": self.user_email,
            "description": self.description,
            "amount": self.amount,
            "status": self.status_text(),
            "status_code": self.status_code,
            "created_at": self.created_at
        }

    def __str__(self):
        return (
            f"Factura #{self.id} | Cliente: {self.user_email} "
            f"| Monto: €{self.amount:.2f} | Estado: {self.status_text()}"
        )


    def status_text(self):
        """
        Devuelve el texto legible del estado de la factura.
        """
        return self.STATUS_OPTIONS.get(self.status_code, "desconocido")

    def to_dict(self):
        """
        Convierte el objeto en un diccionario, útil para guardar o imprimir.
        """
        return {
            "id": self.id,
            "user_email": self.user_email,
            "description": self.description,
            "amount": self.amount,
            "status": self.status_text(),
            "status_code": self.status_code,
            "created_at": self.created_at
        }

    def __str__(self):
        return (
            f"Factura #{self.id} | Cliente: {self.user_email} "
            f"| Monto: €{self.amount:.2f} | Estado: {self.status_text()}"
        )
