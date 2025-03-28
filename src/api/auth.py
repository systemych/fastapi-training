from fastapi import APIRouter, Body, HTTPException, status
from passlib.context import CryptContext
import jwt
from datetime import datetime, timezone, timedelta

from src.database import async_session_maker
from src.schemas.users import UserRegister, UserAdd
from src.repositories.users import UsersRepository
from src.assets.openapi_examples.users import CREATE_USER_EXAMPLE, LOGIN_USER_EXAMPLE

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/register", summary="Создать пользователя")
async def register_user(
    data: UserRegister = Body(openapi_examples=CREATE_USER_EXAMPLE),
):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        user_with_same_email = await UsersRepository(session).get_one_or_none(
            email=data.email
        )
        if user_with_same_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User is existing"
            )
        result = await UsersRepository(session).add(new_user_data)
        await session.commit()
        return result


@router.post("/login", summary="Аутентифицировать пользователя")
async def register_user(
    data: UserRegister = Body(openapi_examples=LOGIN_USER_EXAMPLE),
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(email=data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        access_token = create_access_token({"user_id": user.id})
        return {"access_token": access_token}
