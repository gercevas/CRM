# frontend/services/invoice_services.py

from backend.services.invoice_service import InvoiceService
from frontend.schemas.invoice_schema import InvoiceCreate
from typing import Optional, List

class InvoiceServiceFrontend:
    """
    Servicio puente para facturas desde FastAPI hacia backend.
    """

    def __init__(self):
        self.backend_service = InvoiceService()

    def create_invoice(self, invoice_data: InvoiceCreate) -> Optional[dict]:
        success, factura = self.backend_service.create_invoice(
            user_email=invoice_data.user_email,
            description=invoice_data.description,
            amount_str=str(invoice_data.amount),
            status_code=invoice_data.status_code
        )

        if success:
            return factura.to_dict()
        return None

    def get_invoices_by_user(self, user_email: str) -> List[dict]:
        facturas = self.backend_service.get_invoices_by_user(user_email)
        return [f.to_dict() for f in facturas]

    def get_resumen_by_user(self, user_email: str) -> Optional[dict]:
        resumen = self.backend_service.get_resumen_by_user(user_email)
        if resumen:
            total, monto_total, pagado, pendiente = resumen
            return {
                "total_facturas": total,
                "total_monto": monto_total,
                "total_pagado": pagado,
                "total_pendiente": pendiente
            }
        return None
