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
        phone = input("Ingrese teléfono (opcional): ").strip() or None
        address = input("Ingrese dirección (opcional): ").strip() or None

        success, result = self.service.create_user(
            first_name, last_name, email, phone, address
        )

        if success:
            print("\nUsuario registrado exitosamente!")
            print(f"ID asignado: {result.id}")
            print(f"Fecha de registro: {result.registration_date}")
        else:
            print(f"\nError: {result}")

    def buscar_usuario(self):
        print("\n=== BUSCAR USUARIO ===")
        print("1. Buscar por email")
        print("2. Buscar por nombre")
        criterio = input("Seleccione método de búsqueda: ").strip()

        if criterio == "1":
            email = input("Ingrese email: ").strip()
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
        print("\n=== LISTA DE USUARIOS ===")
        usuarios = self.service.list_users()
        if not usuarios:
            print("No hay usuarios registrados.")
        else:
            for i, user in enumerate(usuarios, start=1):
                print(f"\nUsuario #{i}:")
                self._mostrar_usuario(user)
            print(f"\nTotal de usuarios registrados: {len(usuarios)}")

    def _mostrar_usuario(self, user):
        print("\n--- USUARIO ENCONTRADO ---")
        print(f"ID: {user.id}")
        print(f"Nombre: {user.first_name} {user.last_name}")
        print(f"Email: {user.email}")
        print(f"Teléfono: {user.phone if user.phone else 'No registrado'}")
        print(f"Dirección: {user.address if user.address else 'No registrada'}")
        print(f"Fecha de registro: {user.registration_date}")
