import re

class Validator:
    """
    Clase con métodos estáticos para validar entradas de usuarios y facturas.
    """

    # === Validaciones de Usuario ===
    @staticmethod
    def is_valid_name(name: str) -> bool:
        return bool(name) and name.replace(" ", "").isalpha()

    @staticmethod
    def is_valid_email(email: str) -> bool:
        return bool(re.match(r"^[^@]+@[^@]+\.[^@]+$", email.strip()))

    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        return phone.isdigit() if phone else True

    @staticmethod
    def is_non_empty(value: str) -> bool:
        return bool(value and value.strip())

    # === Validaciones de Factura ===
    @staticmethod
    def is_valid_amount(amount_str: str) -> bool:
        try:
            amount = float(amount_str)
            return amount > 0
        except ValueError:
            return False

    @staticmethod
    def is_valid_description(description: str) -> bool:
        return bool(description and description.strip())

    @staticmethod
    def is_valid_status_code(code: str) -> bool:
        """
        Verifica que el código numérico sea válido: '1', '2' o '3'.
        """
        return code in ["1", "2", "3"]

    @staticmethod
    def is_valid_status(status: str) -> bool:
        """
        Verifica que el estado textual sea válido: 'pendiente', 'pagado' o 'cancelado'.
        """
        return status.lower() in ["pendiente", "pagado", "cancelado"]
