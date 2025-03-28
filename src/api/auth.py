from fastapi import APIRouter, Body, HTTPException, status, Response, Request

from src.database import async_session_maker
from src.schemas.users import UserRegister, UserAdd
from src.repositories.users import UsersRepository
from src.services.auth import AuthService
from src.assets.openapi_examples.users import CREATE_USER_EXAMPLE, LOGIN_USER_EXAMPLE

import json

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/register", summary="Создать пользователя")
async def register_user(
    data: UserRegister = Body(openapi_examples=CREATE_USER_EXAMPLE),
):
    hashed_password = AuthService().hash_password(data.password)
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
    response: Response,
    data: UserRegister = Body(openapi_examples=LOGIN_USER_EXAMPLE),
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(
            email=data.email
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
            )

        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}


@router.get("/only_auth")
async def only_auth(request: Request):
    access_token = (
        request.cookies["access_token"] if "access_token" in request.cookies else None
    )
    return access_token
