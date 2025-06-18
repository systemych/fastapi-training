from fastapi import APIRouter, HTTPException, Path, status
from fastapi_cache.decorator import cache

from src.api.dependencies.user_id import UserIdDep
from src.api.dependencies.db_manager import DBDep
from src.services.options import OptionService
from src.schemas.options import OptionAdd, OptionUpdate
from src.tasks.tasks import test_task
from src.exeptions import AlreadyExistsExeption, NotFoundExeption

router = APIRouter(prefix="/options", tags=["Опции номеров"])


@router.post("/", summary="Добавить опцию")
async def create_option(db: DBDep, user_id: UserIdDep, option_data: OptionAdd):
    try:
        result = await OptionService(db).create_option(option_data)
    except AlreadyExistsExeption as ex:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=ex.detail)

    return result


@router.get("/", summary="Получить список опций")
@cache(expire=60)
async def get_options(db: DBDep, user_id: UserIdDep):
    result = await OptionService(db).get_options()
    return result


@router.put("/{id}", summary="Обновить опцию")
async def update_option(
    db: DBDep,
    user_id: UserIdDep,
    option_data: OptionUpdate,
    id: int = Path(description="ИД опции"),
):
    try:
        result = await OptionService(db).update_option(id=id, option_data=option_data)
    except NotFoundExeption as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.detail)

    return result
