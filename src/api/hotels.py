from fastapi import Query, Path, Body, APIRouter, HTTPException, status

from src.api.dependencies import PaginationDep
from src.database import async_session_maker

from src.schemas.hotels import HotelAdd, HotelUpdate, HotelEdit
from src.repositories.hotels import HotelsRepository
from src.assets.openapi_examples.hotels import (
    CREATE_HOTEL_EXAMPLE,
    UPDATE_HOTEL_EXAMPLE,
    EDIT_HOTEL_EXAMPLE,
)

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/", summary="Получить список отелей")
async def get_hotels(
    pagination: PaginationDep,
    title: str = Query(default=None, description="Название"),
    location: str = Query(default=None, description="Адрес"),
):

    async with async_session_maker() as session:
        result = await HotelsRepository(session).get_all(
            title=title,
            location=location,
            limit=pagination.per_page,
            offset=pagination.per_page * (pagination.page - 1),
        )
        return result


@router.get("/{id}", summary="Получить информацию по отелю")
async def get_hotel(id: int = Path(description="ИД отеля")):
    async with async_session_maker() as session:
        requested_hotel = await HotelsRepository(session).get_one_or_none(id=id)

        if requested_hotel is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            )
        return requested_hotel

@router.post("/", summary="Создать отель")
async def create_hotel(
    hotel_data: HotelAdd = Body(openapi_examples=CREATE_HOTEL_EXAMPLE),
):
    async with async_session_maker() as session:
        result = await HotelsRepository(session).add(hotel_data)
        await session.commit()
        return result


@router.put("/{id}", summary="Обновить все поля отеля")
async def update_hotel(
    id: int = Path(description="ИД отеля"),
    hotel_data: HotelUpdate = Body(openapi_examples=UPDATE_HOTEL_EXAMPLE),
):
    async with async_session_maker() as session:
        requested_hotel = await HotelsRepository(session).get_one_or_none(id=id)

        if requested_hotel is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            )

        result = await HotelsRepository(session).update(hotel_data, id=id)
        await session.commit()
        return result


@router.patch("/{id}", summary="Обновить выбранные поля отеля")
async def edit_hotel(
    id: int = Path(description="ИД отеля"),
    hotel_data: HotelEdit = Body(openapi_examples=EDIT_HOTEL_EXAMPLE),
):
    async with async_session_maker() as session:
        requested_hotel = await HotelsRepository(session).get_one_or_none(id=id)

        if requested_hotel is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            )

        result = await HotelsRepository(session).edit(
            hotel_data, exсlude_unset=True, id=id
        )
        await session.commit()
        return result


@router.delete("/{id}", summary="Удалить отель")
async def delete_hotels(id: int):
    async with async_session_maker() as session:
        requested_hotel = await HotelsRepository(session).get_one_or_none(id=id)

        if requested_hotel is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            )

        await HotelsRepository(session).delete(id=id)
        await session.commit()
    return "OK"
