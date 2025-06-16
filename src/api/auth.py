import logging
from fastapi import APIRouter, Body, HTTPException, status, Response

from src.schemas.users import UserRegister, UserAdd
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep, DBDep
from src.assets.openapi_examples.users import CREATE_USER_EXAMPLE, LOGIN_USER_EXAMPLE


router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/register", summary="Создать пользователя")
async def register_user(
    db: DBDep,
    data: UserRegister = Body(openapi_examples=CREATE_USER_EXAMPLE),
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    user_with_same_email = await db.users.get_one_or_none(email=data.email)
    if user_with_same_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with same email already exist")
    result = await db.users.add(new_user_data)
    await db.commit()
    return result


@router.post("/login", summary="Аутентифицировать пользователя")
async def login_user(
    db: DBDep,
    response: Response,
    data: UserRegister = Body(openapi_examples=LOGIN_USER_EXAMPLE),
):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    access_token = AuthService().create_access_token({"user_id": user.id})
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
    user = await db.users.get_one_or_none(id=user_id)
    return user
