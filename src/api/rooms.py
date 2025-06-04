from datetime import date
from fastapi import Query, Path, Body, APIRouter, HTTPException, status

from src.api.dependencies import DBDep
from src.schemas.rooms import (
    RoomAddRequest,
    RoomAddSchema,
    RoomUpdateRequest,
    RoomUpdateSchema,
    RoomEditRequest,
    RoomEditSchema,
    RoomResponse,
)
from src.schemas.options import RoomsOptionsAdd
from src.assets.openapi_examples.rooms import (
    CREATE_ROOM_EXAMPLE,
    UPDATE_ROOM_EXAMPLE,
    EDIT_ROOM_EXAMPLE,
)

router = APIRouter(prefix="/rooms", tags=["Номера"])


@router.get("/", summary="Получить список номеров отеля")
async def get_rooms(
    db: DBDep,
    hotel_id: int = Query(default=None, example=1, description="ИД отеля"),
    date_from: date = Query(
        default=None, example="2025-01-07", description="Дата заезда"
    ),
    date_to: date = Query(
        default=None, example="2025-01-10", description="Дата выезда"
    ),
):
    result = await db.rooms.get_all(
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
    room_data: RoomAddRequest = Body(openapi_examples=CREATE_ROOM_EXAMPLE),
):
    _room_data = RoomAddSchema(**room_data.model_dump())
    room_id = await db.rooms.add(_room_data)
    await db.flush()
    room = await db.rooms.get_one_or_none(id=room_id)

    if room_data.options_ids:
        room_options = [
            RoomsOptionsAdd(room_id=room.id, option_id=o_id)
            for o_id in room_data.options_ids
        ]
        await db.rooms_options.add_bulk(room_options)
    await db.commit()

    result = RoomResponse(
        options_ids=room_data.options_ids,
        **room.model_dump(exclude_none=True)
    )
    return result


@router.put("/{id}", summary="Обновить все поля номера")
async def update_room(
    db: DBDep,
    id: int = Path(description="ИД номера"),
    updated_room: RoomUpdateRequest = Body(openapi_examples=UPDATE_ROOM_EXAMPLE),
):
    _updated_room = RoomUpdateSchema(**updated_room.model_dump())
    current_room = await db.rooms.get_one_or_none(id=id)

    if current_room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    await db.rooms_options.update(id, updated_room.options_ids)
    await db.rooms.update(_updated_room, id=id)
    await db.commit()

    room_options = await db.rooms_options.get_all(room_id=id)
    updated_room = await db.rooms.get_one_or_none(id=id)

    result = RoomResponse(
        options_ids=[item.option_id for item in room_options],
        **updated_room.model_dump()
    )
    return result


@router.patch("/{id}", summary="Обновить выбранные поля номера")
async def edit_room(
    db: DBDep,
    id: int = Path(description="ИД номера"),
    edited_room: RoomEditRequest = Body(openapi_examples=EDIT_ROOM_EXAMPLE),
):
    _edited_room = RoomEditSchema(**edited_room.model_dump(exclude_unset=True))

    current_room = await db.rooms.get_one_or_none(id=id)
    if current_room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    if edited_room.options_ids:
        await db.rooms_options.update(id, edited_room.options_ids)

    await db.rooms.edit(_edited_room, exсlude_unset=True, id=id)
    await db.commit()

    room_options = await db.rooms_options.get_all(room_id=id)
    updated_room = await db.rooms.get_one_or_none(id=id)

    result = RoomResponse(
        options_ids=[item.option_id for item in room_options],
        **updated_room.model_dump()
    )
    return result


@router.delete("/{id}", summary="Удалить номер")
async def delete_room(db: DBDep, id: int):
    requested_room = await db.rooms.get_one_or_none(id=id)

    if requested_room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    await db.rooms_options.delete_bulk_by_option_id(ids=[option.id for option in requested_room.options])
    await db.rooms.delete(id=id)
    await db.commit()
    return "OK"
