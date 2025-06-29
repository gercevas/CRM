import re

class Validator:
    """
    Clase con métodos estáticos para validar entradas de usuarios y facturas.
    """

    # === Validaciones de Usuario ===
    @staticmethod
    def is_valid_name(name: str) -> bool:
        """
        Verifica que un nombre o apellido contenga solo letras (sin números ni símbolos).
        """
        return bool(name) and name.replace(" ", "").isalpha()

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Verifica que el email tenga al menos un '@' y dominio.
        """
        return bool(re.match(r"^[^@]+@[^@]+\.[^@]+$", email.strip()))

    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        """
        Verifica que el teléfono contenga solo dígitos (o esté vacío).
        """
        return phone.isdigit() if phone else True

    @staticmethod
    def is_non_empty(value: str) -> bool:
        """
        Verifica que un campo obligatorio no esté vacío.
        """
        return bool(value and value.strip())

    # === Validaciones de Factura ===
    @staticmethod
    def is_valid_amount(amount_str: str) -> bool:
        """
        Verifica que el monto sea un número positivo.
        """
        try:
            amount = float(amount_str)
            return amount > 0
        except ValueError:
            return False

    @staticmethod
    def is_valid_status_option(option: str) -> bool:
        """
        Verifica que el estado sea 1 (Pendiente), 2 (Pagada), 3 (Cancelada).
        """
        return option in ["1", "2", "3"]
