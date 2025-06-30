from backend.services.user_service import UserService
from frontend.services.user_services import UserServiceFrontend

def get_user_service(database: str):
    if database == "sql":
        return UserService()
    else:
        return UserServiceFrontend()
