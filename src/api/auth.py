from fastapi import APIRouter, Body, HTTPException, status
from passlib.context import CryptContext

from src.database import async_session_maker
from src.schemas.users import UserRegister, UserAdd
from src.repositories.users import UsersRepository
from src.assets.openapi_examples.users import (
    CREATE_USER_EXAMPLE
)

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", summary="Создать пользователя")
async def register_user(
    data: UserRegister = Body(openapi_examples=CREATE_USER_EXAMPLE),
):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        user_with_same_email = await UsersRepository(session).get_one_or_none(email=data.email)
        if user_with_same_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User is existing"
            )
        result = await UsersRepository(session).add(new_user_data)
        await session.commit()
        return result