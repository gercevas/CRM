from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class InvoiceCreate(BaseModel):
    user_email: str = Field(..., example="usuario@example.com")
    description: str = Field(..., example="Consultoría de datos")
    amount: float = Field(..., gt=0, example=250.0)
    status_code: str = Field(..., pattern="^(1|2|3)$", example="1") # 1: Pendiente, 2: Pagada, 3: Cancelada
  
class InvoiceResponse(BaseModel):
    id: str
    user_email: EmailStr
    description: str
    amount: float
    status_code: str
    status: str
    created_at: str

    class Config:
        from_attribues = True
class ResumenFinanciero(BaseModel):
    total_facturas: int
    total_monto: float
    total_pagado: float
    total_pendiente: float
