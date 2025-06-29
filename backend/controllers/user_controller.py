from backend.services.user_service import UserService


class UserController:
    """
    Controlador para manejar las acciones relacionadas con usuarios.
    """

    def __init__(self):
        self.service = UserService()

    def registrar_usuario(self):
        print("\n=== REGISTRO DE NUEVO USUARIO ===")
        first_name = input("Ingrese nombre: ").strip()
        last_name = input("Ingrese apellidos: ").strip()
        email = input("Ingrese email: ").strip()
        phone = input("Ingrese teléfono (opcional): ").strip()
        phone = phone if phone else None
        address = input("Ingrese dirección (opcional): ").strip()
        address = address if address else None

        success, result = self.service.create_user(
            first_name, last_name, email, phone, address
        )

        if success:
            print("\nUsuario registrado exitosamente!")
            print(f"ID asignado: {result.id}")
            print(f"Fecha de registro: {result.registration_date.strftime('%d/%m/%Y')}")
        else:
            print(f"\nError: {result}")

    def buscar_usuario(self):
        criterio = input("Buscar por (1) Email o (2) Nombre: ").strip()
        if criterio == "1":
            email = input("Ingrese el email del usuario: ").strip()
            user = self.service.find_by_email(email)
            if user:
                self._mostrar_usuario(user)
            else:
                print("Usuario no encontrado.")
        elif criterio == "2":
            nombre = input("Ingrese el nombre o apellido: ").strip()
            usuarios = self.service.find_by_name(nombre)
            if usuarios:
                for user in usuarios:
                    self._mostrar_usuario(user)
            else:
                print("No se encontraron usuarios con ese nombre.")
        else:
            print("Opción inválida.")

    def mostrar_usuarios(self):
        usuarios = self.service.list_users()
        if not usuarios:
            print("No hay usuarios registrados.")
        else:
            for user in usuarios:
                self._mostrar_usuario(user)

    def _mostrar_usuario(self, user):
        print("\n--- Usuario ---")
        print(f"ID: {user.id}")
        print(f"Nombre: {user.first_name} {user.last_name}")
        print(f"Email: {user.email}")
        print(f"Teléfono: {user.phone if user.phone else 'No registrado'}")
        print(f"Dirección: {user.address if user.address else 'No registrada'}")
        print(f"Registrado el: {user.registration_date.strftime('%d/%m/%Y')}")
