from fastapi import FastAPI
from frontend.routers import user_router, invoice_router

app = FastAPI(
    title="Sistema CRM - API",
    description="API para gestionar usuarios y facturas en un sistema CRM",
    version="1.0.0"
)

# Incluir routers
app.include_router(user_router.router)
app.include_router(invoice_router.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API del CRM. Visita /docs para ver la documentación."}

@app.get("/health")
def health_check():
    return {"status": "ok"}
