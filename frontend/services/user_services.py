# frontend/services/user_services.py

from backend.services.user_service import UserService
from frontend.schemas.user_schema import UserCreate
from typing import Optional, List
from backend.models.user import User

class UserServiceFrontend:
    """
    Servicio puente entre el frontend (API) y el backend real.
    """

    def __init__(self):
        self.backend_service = UserService()

    def create_user(self, user_data: UserCreate) -> Optional[dict]:
        """
        Crea un nuevo usuario usando la lógica del backend.
        Devuelve un diccionario con los datos del usuario o None si falló.
        """
        success, user = self.backend_service.create_user(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            phone=user_data.phone,
            address=user_data.address
        )

        if success:
            return user.to_dict()
        return None

    def find_by_email(self, email: str) -> Optional[dict]:
        """
        Busca un usuario por email y devuelve su representación como dict.
        """
        user = self.backend_service.find_by_email(email)
        return user.to_dict() if user else None

    def list_users(self) -> List[dict]:
        """
        Devuelve todos los usuarios como lista de diccionarios.
        """
        users = self.backend_service.list_users()
        return [user.to_dict() for user in users]
