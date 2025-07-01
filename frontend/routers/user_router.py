from fastapi import APIRouter, HTTPException, Query
from frontend.schemas.user_schema import UserCreate, UserResponse
from frontend.services import database_selector
from typing import List

router = APIRouter(prefix="/users", tags=["Usuarios"])

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, database: str = Query("sql")):
    service = database_selector.get_user_service(database)
    success, result = service.create_user(
        user.first_name,
        user.last_name,
        user.email,
        user.phone,
        user.address
    )
    if not success:
        raise HTTPException(status_code=400, detail=result)
    return result

@router.get("/", response_model=List[UserResponse])
def list_users(database: str = Query("sql")):
    service = database_selector.get_user_service(database)
    return service.list_users()

@router.get("/{email}", response_model=UserResponse)
def get_user_by_email(email: str, database: str = Query("sql")):
    service = database_selector.get_user_service(database)
    user = service.find_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return user
