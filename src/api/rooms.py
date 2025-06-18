from datetime import date
from fastapi import Query, Path, Body, APIRouter, HTTPException, status

from src.api.dependencies.db_manager import DBDep
from src.schemas.rooms import (
    RoomAddRequest,
    RoomUpdateRequest,
    RoomEditRequest,
)
from src.services.rooms import RoomService
from src.exeptions import DataValidationExeption, NotFoundExeption
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
    date_from: date = Query(default=None, example="2025-01-07", description="Дата заезда"),
    date_to: date = Query(default=None, example="2025-01-10", description="Дата выезда"),
):
    try:
        result = await RoomService(db).get_rooms(hotel_id, date_from, date_to)
    except DataValidationExeption as ex:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=ex.detail,
        )

    return result


@router.get("/{id}", summary="Получить информацию по номеру")
async def get_room(
    db: DBDep,
    id: int = Path(description="ИД комнаты"),
):
    try:
        requested_room = await RoomService(db).get_room(id)
    except NotFoundExeption as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.detail)

    return requested_room


@router.post("/", summary="Создать номер в отеле")
async def create_room(
    db: DBDep,
    room_data: RoomAddRequest = Body(openapi_examples=CREATE_ROOM_EXAMPLE),
):
    try:
        result = await RoomService(db).create_room(room_data)
    except NotFoundExeption as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.detail)

    return result


@router.put("/{id}", summary="Обновить все поля номера")
async def update_room(
    db: DBDep,
    id: int = Path(description="ИД номера"),
    updated_room: RoomUpdateRequest = Body(openapi_examples=UPDATE_ROOM_EXAMPLE),
):
    try:
        result = await RoomService(db).update_room(id, updated_room)
    except NotFoundExeption as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.detail)

    return result


@router.patch("/{id}", summary="Обновить выбранные поля номера")
async def edit_room(
    db: DBDep,
    id: int = Path(description="ИД номера"),
    edited_room: RoomEditRequest = Body(openapi_examples=EDIT_ROOM_EXAMPLE),
):
    try:
        result = await RoomService(db).edit_room(id, edited_room)
    except NotFoundExeption as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.detail)

    return result


@router.delete("/{id}", summary="Удалить номер")
async def delete_room(db: DBDep, id: int):
    try:
        await RoomService(db).delete_room(id)
    except NotFoundExeption as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.detail)

    return "OK"
