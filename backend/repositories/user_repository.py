# backend/repositories/user_repository.py

from backend.models.user import User
from backend.utils.singleton import Singleton

class UserRepository(metaclass=Singleton):
    """
    Repositorio que gestiona el almacenamiento y recuperación de usuarios.
    Implementado como Singleton para mantener consistencia en memoria.
    """

    def __init__(self):
        self.users = []

    def save_user(self, user: User):
        self.users.append(user)

    def find_by_email(self, email: str):
        email = email.strip().lower()
        for user in self.users:
            if user.email.lower() == email:
                return user
        return None

    def find_by_name(self, name: str):
        name = name.strip().lower()
        return [
            user for user in self.users
            if name in user.first_name.lower() or name in user.last_name.lower()
        ]

    def list_users(self):
        return self.users

    def list_all(self):
        return self.users

    def get_next_user_id(self):
        return f"USR{len(self.users) + 1:03d}"
