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

    def create_invoice(self, user_email, description, amount_str, status_code):
        """
        Crea una nueva factura asociada a un usuario existente.
        """
        try:
            user_email = str(user_email).strip().lower()
            description = str(description).strip()
            
            if not user_email:
                return False, "El email no puede estar vacío."
                
            if not description:
                return False, "La descripción no puede estar vacía."

            try:
                amount = float(amount_str)
                if amount <= 0:
                    return False, "El monto debe ser un número positivo."
            except (ValueError, TypeError):
                return False, "El monto debe ser un número válido."

            if not status_code or str(status_code) not in ["1", "2", "3"]:
                return False, "El estado debe ser 1 (Pendiente), 2 (Pagada) o 3 (Cancelada)."
            
            if not self.user_repo.find_by_email(user_email):
                return False, "No existe un usuario con ese email."

            invoice_id = self.repo.get_next_invoice_id()
            
            invoice = Invoice(
                id=invoice_id,
                user_email=user_email,
                description=description,
                amount=amount,
                status_code=str(status_code)
            )

            self.repo.save_invoice(invoice)
            return True, invoice
            
        except Exception as e:
            return False, f"Error inesperado al crear la factura: {str(e)}"

    def get_invoices_by_user(self, user_email):
        return self.repo.find_by_user(user_email)

    def get_resumen_by_user(self, user_email):
        return self.repo.resumen_financiero_por_usuario(user_email)