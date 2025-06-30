# frontend/routers/invoice_router.py

from fastapi import APIRouter, HTTPException, Query
from frontend.schemas.invoice_schema import InvoiceCreate, InvoiceResponse, ResumenFinanciero
from frontend.services.invoice_services import InvoiceServiceFrontend
from typing import List

router = APIRouter(prefix="/invoices", tags=["Facturas"])
service = InvoiceServiceFrontend()

@router.post("/", response_model=InvoiceResponse)
def create_invoice(invoice_data: InvoiceCreate, database: str = Query("sql")):
    factura = service.create_invoice(invoice_data)
    if not factura:
        raise HTTPException(status_code=400, detail="No se pudo crear la factura.")
    return factura

@router.get("/", response_model=List[InvoiceResponse])
def list_by_user(user_email: str, database: str = Query("sql")):
    facturas = service.get_invoices_by_user(user_email)
    return facturas

@router.get("/resumen", response_model=ResumenFinanciero)
def resumen_por_usuario(user_email: str, database: str = Query("sql")):
    resumen = service.get_resumen_by_user(user_email)
    if resumen is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o sin facturas.")
    return resumen
