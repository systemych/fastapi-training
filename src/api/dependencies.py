from typing import Annotated
from fastapi import Query, Depends, Request, HTTPException, status
from pydantic import BaseModel

from src.services.auth import AuthService

# Query в Query - баг FastAPI, в OpenAPI не отображается description при использовании Depends.
# Тема: https://github.com/fastapi/fastapi/issues/4700
# Решение: https://github.com/fastapi/fastapi/issues/4700#issuecomment-1149404526
# Если используется default, то троеточие не нужно.
# Fix по этой теме до сих пор открыт: https://github.com/fastapi/fastapi/pull/4573

class PaginationParams(BaseModel):
    page: Annotated[int, Query(Query(default=1, ge=1, description="Страница пагинации"))]
    per_page: Annotated[int, Query(Query(default=3, ge=1, le=10, description="Объектов на странице"))]

PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request):
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Вы не предоставили токен доступа")
    return token

def get_current_user_id(token: str = Depends(get_token)) -> int:
    user_data = AuthService().decode_token(token)
    return user_data.get("user_id")

UserIdDep = Annotated[int, Depends(get_current_user_id)]