from backend.controllers.user_controller import UserController
from backend.controllers.invoice_controller import InvoiceController


def mostrar_menu():
    print("\n=== SISTEMA CRM ===")
    print("1. Registrar nuevo usuario")
    print("2. Buscar usuario")
    print("3. Crear factura para usuario")
    print("4. Mostrar todos los usuarios")
    print("5. Mostrar facturas de un usuario")
    print("6. Resumen financiero por usuario")
    print("7. Salir")


def main():
    user_controller = UserController()
    invoice_controller = InvoiceController()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            user_controller.registrar_usuario()
        elif opcion == "2":
            user_controller.buscar_usuario()
        elif opcion == "3":
            invoice_controller.crear_factura()
        elif opcion == "4":
            user_controller.mostrar_usuarios()
        elif opcion == "5":
            invoice_controller.mostrar_facturas_usuario()
        elif opcion == "6":
            invoice_controller.mostrar_resumen_usuario()
        elif opcion == "7":
            print("Gracias por usar el sistema CRM. ¡Hasta pronto!")
            break
        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    main()
