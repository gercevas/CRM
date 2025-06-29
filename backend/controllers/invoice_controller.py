from backend.services.invoice_service import InvoiceService


class InvoiceController:
    """
    Controlador para manejar la interacción por consola sobre facturas.
    """

    def __init__(self):
        self.service = InvoiceService()

    def crear_factura(self):
        print("\n=== CREAR FACTURA ===")
        user_email = input("Ingrese el email del usuario: ").strip()
        description = input("Ingrese descripción del servicio/producto: ").strip()
        amount = input("Ingrese monto total: ").strip()
        status = input("Estado (pendiente/pagado): ").strip().lower()

        success, result = self.service.create_invoice(user_email, description, amount, status)

        if success:
            print("\nFactura creada exitosamente!")
            print(result)
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
            for f in facturas:
                print(f)

    def mostrar_resumen_usuario(self):
        print("\n=== RESUMEN FINANCIERO ===")
        user_email = input("Ingrese el email del usuario: ").strip()
        resumen = self.service.get_resumen_by_user(user_email)

        if resumen:
            total, monto_total, pagado, pendiente = resumen
            print(f"\nUsuario: {user_email}")
            print(f"- Total facturas: {total}")
            print(f"- Monto total: {monto_total or 0:.2f} €")
            print(f"- Pagado: {pagado or 0:.2f} €")
            print(f"- Pendiente: {pendiente or 0:.2f} €")
        else:
            print("No se encontró información financiera para este usuario.")
