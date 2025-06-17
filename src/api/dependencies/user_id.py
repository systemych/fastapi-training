from typing import Annotated
from fastapi import Depends, Request, HTTPException, status

from src.services.auth import AuthService

def get_token(request: Request):
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Вы не предоставили токен доступа",
        )
    return token

def get_current_user_id(token: str = Depends(get_token)) -> int:
    user_data = AuthService().decode_token(token)
    return user_data.get("user_id")


UserIdDep = Annotated[int, Depends(get_current_user_id)]