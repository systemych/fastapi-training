from datetime import date
from fastapi import Query, Path, Body, APIRouter, HTTPException, status

from src.api.dependencies.pagination import PaginationDep
from src.api.dependencies.db_manager import DBDep
from src.schemas.hotels import HotelAdd, HotelUpdate, HotelEdit
from src.assets.openapi_examples.hotels import (
    CREATE_HOTEL_EXAMPLE,
    UPDATE_HOTEL_EXAMPLE,
    EDIT_HOTEL_EXAMPLE,
)
from src.services.hotels import HotelService
from src.exeptions import DataValidationExeption, NotFoundExeption

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/", summary="Получить список отелей")
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str = Query(default=None, description="Название"),
    location: str = Query(default=None, description="Адрес"),
    date_from: date = Query(default=None, description="Дата начала для заезда"),
    date_to: date = Query(default=None, description="Дата окончания для заезда"),
):
    try:
        result = await HotelService(db).get_hotels(
            pagination, title, location, date_from, date_to
        )
    except DataValidationExeption as ex:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=ex.detail,
        )

    return result


@router.get("/{id}", summary="Получить информацию по отелю")
async def get_hotel(db: DBDep, id: int = Path(description="ИД отеля")):
    try:
        requested_hotel = await HotelService(db).get_hotel(id)
    except NotFoundExeption as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.detail)

    return requested_hotel


@router.post("/", summary="Создать отель")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(openapi_examples=CREATE_HOTEL_EXAMPLE),
):
    result = await HotelService(db).create_hotel(hotel_data)
    return result


@router.put("/{id}", summary="Обновить все поля отеля")
async def update_hotel(
    db: DBDep,
    id: int = Path(description="ИД отеля"),
    hotel_data: HotelUpdate = Body(openapi_examples=UPDATE_HOTEL_EXAMPLE),
):
    try:
        result = await HotelService(db).update_hotel(id, hotel_data)
    except NotFoundExeption as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.detail)

    return result


@router.patch("/{id}", summary="Обновить выбранные поля отеля")
async def edit_hotel(
    db: DBDep,
    id: int = Path(description="ИД отеля"),
    hotel_data: HotelEdit = Body(openapi_examples=EDIT_HOTEL_EXAMPLE),
):
    try:
        result = await HotelService(db).edit_hotel(id, hotel_data)
    except NotFoundExeption as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.detail)

    return result


@router.delete("/{id}", summary="Удалить отель")
async def delete_hotels(db: DBDep, id: int):
    try:
        await HotelService(db).delete_hotels(id)
    except NotFoundExeption:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found"
        )

    return "OK"
