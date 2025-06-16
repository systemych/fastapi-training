from fastapi import APIRouter, HTTPException, Path, status
from fastapi_cache.decorator import cache

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.options import OptionAdd, OptionUpdate
from src.tasks.tasks import test_task

router = APIRouter(prefix="/options", tags=["Опции номеров"])


@router.post("/", summary="Добавить опцию")
async def create_option(db: DBDep, user_id: UserIdDep, option_data: OptionAdd):
    option = await db.options.get_one_or_none(title=option_data.title)
    if option:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Item already exist"
        )

    result = await db.options.add(option_data)
    await db.commit()
    return result


@router.get("/", summary="Получить список опций")
@cache(expire=60)
async def get_options(db: DBDep, user_id: UserIdDep):
    test_task.delay()
    return await db.options.get_all()


@router.put("/{id}", summary="Обновить опцию")
async def update_option(
    db: DBDep,
    user_id: UserIdDep,
    option_data: OptionUpdate,
    id: int = Path(description="ИД опции"),
):
    option = await db.options.get_one_or_none(id=id)
    if option is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    result = await db.options.update(option_data, id=id)
    return result
