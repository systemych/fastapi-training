from typing import Annotated
from fastapi import Query, Depends
from pydantic import BaseModel


# Query в Query - баг FastAPI, в OpenAPI не отображается description при использовании Depends.
# Тема: https://github.com/fastapi/fastapi/issues/4700
# Решение: https://github.com/fastapi/fastapi/issues/4700#issuecomment-1149404526
# Если используется default, то троеточие не нужно.
# Fix по этой теме до сих пор открыт: https://github.com/fastapi/fastapi/pull/4573

class PaginationParams(BaseModel):
    page: Annotated[int, Query(Query(default=1, ge=1, description="Страница пагинации"))]
    per_page: Annotated[
        int, Query(Query(default=3, ge=1, le=10, description="Объектов на странице"))
    ]


PaginationDep = Annotated[PaginationParams, Depends()]