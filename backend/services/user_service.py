from backend.models.user import User
from backend.utils.validators import Validator
from backend.repositories.user_repository import UserRepository

class UserService:
    """
    Servicio que gestiona la lógica de negocio para usuarios.
    """

    def __init__(self):
        self.repo = UserRepository()

    def create_user(self, first_name, last_name, email, phone=None, address=None):
        """
        Crea y guarda un nuevo usuario si es válido. Devuelve el usuario creado o error.
        """
        # Validaciones
        if not Validator.is_valid_name(first_name):
            return False, "Nombre inválido. Solo se permiten letras."
        if not Validator.is_valid_name(last_name):
            return False, "Apellidos inválidos. Solo se permiten letras."
        if not Validator.is_valid_email(email):
            return False, "Email inválido. Debe tener formato correcto."
        if self.repo.find_by_email(email):
            return False, "Ya existe un usuario con ese email."
        if not Validator.is_valid_phone(phone):
            return False, "Teléfono inválido. Solo se permiten números."

        # Generar ID
        next_id = self._generate_next_id()
        user = User(
            id=next_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address
        )

        self.repo.save_user(user)
        return True, user

    def _generate_next_id(self):
        """
        Genera el próximo ID de usuario en formato USR001, USR002, ...
        """
        users = self.repo.list_users()
        if not users:
            return "USR001"

        last_ids = [int(u.id.replace("USR", "")) for u in users if u.id.startswith("USR")]
        next_num = max(last_ids) + 1
        return f"USR{next_num:03}"

    def list_users(self):
        """
        Devuelve todos los usuarios.
        """
        return self.repo.list_users()

    def find_by_email(self, email):
        """
        Busca un usuario por email.
        """
        return self.repo.find_by_email(email)

    def find_by_name(self, name):
        """
        Busca usuarios cuyo nombre o apellido contengan cierto texto.
        """
        return self.repo.find_by_name(name)
