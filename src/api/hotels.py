from fastapi import Query, Path, Body, APIRouter, Depends
from sqlalchemy import insert, select, update, delete

from src.api.dependencies import PaginationDep
from src.database import async_session_maker

from src.schemas.hotels import HotelPOST, HotelPUT, HotelPATCH
from src.models.hotels import HotelsOrm
from src.repositories.hotels import HotelsRepository
from src.assets.openapi_examples.hotels import (
    POST_OPENAPI_EXAMPLE,
    PUT_OPENAPI_EXAMPLE,
    PATCH_OPENAPI_EXAMPLE,
)

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/hotels", summary="Получить список отелей")
async def get_hotels(
    pagination: PaginationDep,
    title: str = Query(default=None, description="Название"),
    location: str = Query(default=None, description="Адрес"),
):

    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            title=title,
            location=location,
            limit=pagination.per_page,
            offset=pagination.per_page * (pagination.page - 1),
        )


@router.get("/hotels/{id}", summary="Получить информацию по отелю")
async def get_hotel(id: int = Path(description="ИД отеля")):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=id)


@router.post("/hotels", summary="Создать отель")
async def create_hotel(
    hotel_data: HotelPOST = Body(openapi_examples=POST_OPENAPI_EXAMPLE),
):
    async with async_session_maker() as session:
        result = await HotelsRepository(session).add(**hotel_data.model_dump())
        await session.flush()
        id = result.scalars().one_or_none()
        await session.commit()
        return await HotelsRepository(session).get_one_or_none(id=id)


@router.put("/hotels/{id}", summary="Обновить все поля отеля")
async def update_hotel(
    id: int = Path(description="ИД отеля"),
    hotel_data: HotelPUT = Body(openapi_examples=PUT_OPENAPI_EXAMPLE),
):
    async with async_session_maker() as session:
        update_hotel_stmt = (
            update(HotelsOrm).filter_by(id=id).values(**hotel_data.model_dump())
        )
        await session.execute(update_hotel_stmt)
        await session.commit()
    return hotel_data.model_dump()


@router.patch("/hotels/{id}", summary="Обновить выбранные поля отеля")
async def edit_hotel(
    id: int = Path(description="ИД отеля"),
    hotel_data: HotelPATCH = Body(openapi_examples=PATCH_OPENAPI_EXAMPLE),
):
    async with async_session_maker() as session:
        edit_hotel_stmt = update(HotelsOrm).filter_by(id=id)

        if hotel_data.title:
            edit_hotel_stmt = edit_hotel_stmt.values(title=hotel_data.title)
        if hotel_data.location:
            edit_hotel_stmt = edit_hotel_stmt.values(title=hotel_data.location)

        await session.execute(edit_hotel_stmt)
        await session.commit()

        query = select(HotelsOrm).filter_by(id=id)

        result = await session.execute(query)
        hotel = result.scalars().all()
        return hotel


@router.delete("/hotels/{id}", summary="Удалить отель")
async def delete_hotels(id: int):
    async with async_session_maker() as session:
        delete_hotel_stmt = delete(HotelsOrm).filter_by(id=id)
        await session.execute(delete_hotel_stmt)
        await session.commit()
    return {"status": "OK"}
