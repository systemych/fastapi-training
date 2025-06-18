import logging
from fastapi import APIRouter, Body, HTTPException, status, Response

from src.schemas.users import UserRegister
from src.services.auth import AuthService
from src.api.dependencies.user_id import UserIdDep
from src.api.dependencies.db_manager import DBDep
from src.exeptions import AlreadyExistsExeption, NotFoundExeption, BadCredentialsExeption
from src.assets.openapi_examples.users import CREATE_USER_EXAMPLE, LOGIN_USER_EXAMPLE


router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/register", summary="Создать пользователя")
async def register_user(
    db: DBDep,
    data: UserRegister = Body(openapi_examples=CREATE_USER_EXAMPLE),
):
    try:
        result = await AuthService(db).register_user(data)
    except AlreadyExistsExeption as ex:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=ex.detail)

    return result


@router.post("/login", summary="Аутентифицировать пользователя")
async def login_user(
    db: DBDep,
    response: Response,
    data: UserRegister = Body(openapi_examples=LOGIN_USER_EXAMPLE),
):
    try:
        access_token = await AuthService(db).login_user(data)
    except NotFoundExeption as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.detail)
    except BadCredentialsExeption as ex:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ex.detail)

    response.set_cookie("access_token", access_token)
    logging.info(f"Пользователь {data.email} аутентифицирован")
    return {"access_token": access_token}


@router.post("/logout", summary="Убрать аутентификацию пользователя")
async def logout_user(
    response: Response,
):
    try:
        response.delete_cookie("access_token")
    except Exception:
        pass
    return "OK"


@router.get("/me", summary="Получить информацию по пользователю")
async def get_me(db: DBDep, user_id: UserIdDep):
    user = await AuthService(db).get_me(user_id)
    return user
