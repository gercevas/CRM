from datetime import datetime

class User:
    """
    Clase que representa a un usuario (cliente) en el sistema CRM.
    """

    def __init__(self, id, first_name, last_name, email, phone=None, address=None, registration_date=None):
        self.id = id  # Este puede ser generado automáticamente por la BBDD
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email.strip().lower()
        self.phone = phone
        self.address = address
        self.registration_date = registration_date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def to_dict(self):
        """
        Convierte el objeto en un diccionario. Útil para serialización o impresión.
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "registration_date": self.registration_date
        }

    def __str__(self):
        return f"{self.full_name()} ({self.email}) - Registrado el {self.registration_date}"
