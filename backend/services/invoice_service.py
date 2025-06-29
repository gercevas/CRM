from backend.models.invoice import Invoice
from backend.repositories.invoice_repository import InvoiceRepository
from backend.repositories.user_repository import UserRepository
from backend.utils.validators import Validator


class InvoiceService:
    """
    Servicio que gestiona la lógica de negocio relacionada con facturas.
    """

    def __init__(self):
        self.repo = InvoiceRepository()
        self.user_repo = UserRepository()

    def create_invoice(self, user_id, description, amount_str, status):
        """
        Crea una nueva factura asociada a un usuario existente.
        """

        # Validaciones
        if not Validator.is_valid_description(description):
            return False, "La descripción no puede estar vacía."

        if not Validator.is_valid_amount(amount_str):
            return False, "El monto debe ser un número positivo."

        if not Validator.is_valid_status(status):
            return False, "El estado debe ser 'pendiente' o 'pagado'."

        if not self.user_repo.find_by_email(user_id):
            return False, "No existe un usuario con ese email."

        # Convertir monto
        amount = float(amount_str)

        # Generar ID
        invoice_id = self.repo.get_next_invoice_id()

        invoice = Invoice(
            id=invoice_id,
            user_id=user_id,
            description=description,
            amount=amount,
            status=status.lower()
        )

        self.repo.save_invoice(invoice)
        return True, invoice

    def get_invoices_by_user(self, user_id):
        return self.repo.find_by_user(user_id)

    def get_resumen_by_user(self, user_id):
        return self.repo.resumen_financiero_por_usuario(user_id)
