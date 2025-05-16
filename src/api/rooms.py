from datetime import date
from fastapi import Query, Path, Body, APIRouter, HTTPException, status

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomUpdate, RoomEdit
from src.assets.openapi_examples.rooms import (
    CREATE_ROOM_EXAMPLE,
    UPDATE_ROOM_EXAMPLE,
    EDIT_ROOM_EXAMPLE,
)

router = APIRouter(prefix="/rooms", tags=["Номера"])


@router.get("/", summary="Получить список номеров отеля")
async def get_rooms(
    db: DBDep,
    hotel_id: int = Query(default=None, description="ИД отеля"),
    date_from: date = Query(example="2025-01-07"),
    date_to: date = Query(example="2025-01-10"),
):
    result = await db.rooms.get_all_by_date(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )
    return result


@router.get("/{id}", summary="Получить информацию по номеру")
async def get_room(
    db: DBDep,
    id: int = Path(description="ИД комнаты"),
):
    requested_room = await db.rooms.get_one_or_none(id=id)

    if requested_room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return requested_room


@router.post("/", summary="Создать номер в отеле")
async def create_room(
    db: DBDep,
    room_data: RoomAdd = Body(openapi_examples=CREATE_ROOM_EXAMPLE),
):
    result = await db.rooms.add(room_data)
    await db.commit()
    return result


@router.put("/{id}", summary="Обновить все поля номера")
async def update_room(
    db: DBDep,
    id: int = Path(description="ИД номера"),
    room_data: RoomUpdate = Body(openapi_examples=UPDATE_ROOM_EXAMPLE),
):
    requested_room = await db.rooms.get_one_or_none(id=id)

    if requested_room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    result = await db.rooms.update(room_data, id=id)
    await db.commit()
    return result


@router.patch("/{id}", summary="Обновить выбранные поля номера")
async def edit_room(
    db: DBDep,
    id: int = Path(description="ИД номера"),
    room_data: RoomEdit = Body(openapi_examples=EDIT_ROOM_EXAMPLE),
):
    requested_room = await db.rooms.get_one_or_none(id=id)

    if requested_room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    result = await db.rooms.edit(room_data, exсlude_unset=True, id=id)
    await db.commit()
    return result


@router.delete("/{id}", summary="Удалить номер")
async def delete_room(db: DBDep, id: int):
    requested_room = await db.rooms.get_one_or_none(id=id)

    if requested_room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    await db.rooms.delete(id=id)
    await db.commit()
    return "OK"
