from fastapi import Query, Path, Body, APIRouter, HTTPException, status

from src.database import async_session_maker

from src.schemas.rooms import RoomAdd, RoomUpdate, RoomEdit
from src.repositories.rooms import RoomsRepository
from src.assets.openapi_examples.rooms import CREATE_ROOM_EXAMPLE, UPDATE_ROOM_EXAMPLE, EDIT_ROOM_EXAMPLE

router = APIRouter(prefix="/rooms", tags=["Номера"])


@router.get("/", summary="Получить список номеров отеля")
async def get_rooms(hotel_id: int = Query(default=None, description="ИД отеля")):
    async with async_session_maker() as session:
        result = await RoomsRepository(session).get_all(hotel_id=hotel_id)
        return result


@router.get("/{id}", summary="Получить информацию по номеру")
async def get_room(
    id: int = Path(description="ИД комнаты"),
):
    async with async_session_maker() as session:
        requested_room = await RoomsRepository(session).get_one_or_none(id=id)

        if requested_room is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            )
        return requested_room


@router.post("/", summary="Создать номер в отеле")
async def create_room(
    room_data: RoomAdd = Body(openapi_examples=CREATE_ROOM_EXAMPLE),
):
    async with async_session_maker() as session:
        result = await RoomsRepository(session).add(room_data)
        await session.commit()
        return result


@router.put("/{id}", summary="Обновить все поля номера")
async def update_room(
    id: int = Path(description="ИД номера"),
    room_data: RoomUpdate = Body(openapi_examples=UPDATE_ROOM_EXAMPLE),
):
    async with async_session_maker() as session:
        requested_room = await RoomsRepository(session).get_one_or_none(id=id)

        if requested_room is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            )

        result = await RoomsRepository(session).update(room_data, id=id)
        await session.commit()
        return result


@router.patch("/{id}", summary="Обновить выбранные поля номера")
async def edit_room(
    id: int = Path(description="ИД номера"),
    room_data: RoomEdit = Body(openapi_examples=EDIT_ROOM_EXAMPLE),
):
    async with async_session_maker() as session:
        requested_room = await RoomsRepository(session).get_one_or_none(id=id)

        if requested_room is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            )

        result = await RoomsRepository(session).edit(
            room_data, exсlude_unset=True, id=id
        )
        await session.commit()
        return result


@router.delete("/{id}", summary="Удалить номер")
async def delete_room(id: int):
    async with async_session_maker() as session:
        requested_room = await RoomsRepository(session).get_one_or_none(id=id)

        if requested_room is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            )

        await RoomsRepository(session).delete(id=id)
        await session.commit()
    return "OK"