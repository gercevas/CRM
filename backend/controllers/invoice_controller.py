from backend.services.invoice_service import InvoiceService
from backend.repositories.user_repository import UserRepository

class InvoiceController:
    """
    Controlador para manejar la interacción por consola sobre facturas.
    """

    def __init__(self):
        self.service = InvoiceService()

    def crear_factura(self):
        print("\n=== CREACIÓN DE FACTURA PARA USUARIO ===")
        user_email = input("Ingrese el email del usuario: ").strip()
        
        if not user_email:
            print("Error: El email no puede estar vacío.")
            return
            
        description = input("Ingrese descripción del servicio/producto: ").strip()

        try:
            amount_str = input("Ingrese monto total (€): ").strip()
            amount = float(amount_str)
        except ValueError:
            print("Error: El monto debe ser un número válido.")
            return

        print("Seleccione estado:")
        print("1. Pendiente")
        print("2. Pagada")
        print("3. Cancelada")
        estado_opcion = input("Estado (1-3): ").strip()

        estados = {
            "1": "1",
            "2": "2",
            "3": "3"
        }

        status_code = estados.get(estado_opcion)

        if not status_code:
            print("Error: Opción inválida. Debe seleccionar 1, 2 o 3.")
            return

        success, result = self.service.create_invoice(user_email, description, amount_str, status_code)

        if success:
            print("\nFactura creada exitosamente!")
            print("--- Detalles de la factura ---")
            print(f"ID: {result.id}")
            print(f"Descripción: {result.description}")
            print(f"Monto: {result.amount:.2f} €")
            print(f"Estado: {result.status_text()}")
            print(f"Fecha: {result.issue_date}")
        else:
            print(f"\nError al crear factura: {result}")

    def mostrar_facturas_usuario(self):
        print("\n=== FACTURAS DE UN USUARIO ===")
        user_email = input("Ingrese el email del usuario: ").strip()
        facturas = self.service.get_invoices_by_user(user_email)

        if not facturas:
            print("No se encontraron facturas para ese usuario.")
        else:
            print(f"\n--- FACTURAS DE {user_email} ---")
            for i, f in enumerate(facturas, start=1):
                print(f"\nFactura #{i}")
                print(f"- ID: {f.id}")
                print(f"- Descripción: {f.description}")
                print(f"- Monto: {f.amount:.2f} €")
                print(f"- Estado: {f.status_text()}")
                print(f"- Fecha: {f.issue_date}")

    def mostrar_resumen_usuario(self):
        print("\n=== RESUMEN FINANCIERO POR USUARIO ===")
        user_email = input("Ingrese el email del usuario: ").strip()
        resumen = self.service.get_resumen_by_user(user_email)

        if resumen:
            total, monto_total, pagado, pendiente = resumen
            print(f"\n--- Resumen financiero de {user_email} ---")
            print(f"- Total de facturas: {total}")
            print(f"- Monto total facturado: {monto_total or 0:.2f} €")
            print(f"- Total pagado: {pagado or 0:.2f} €")
            print(f"- Total pendiente: {pendiente or 0:.2f} €")
        else:
            print("No se encontró información financiera para este usuario.")