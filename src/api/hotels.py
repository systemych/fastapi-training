from fastapi import Query, Path, Body, APIRouter, Depends
from sqlalchemy import insert, select

from src.api.dependencies import PaginationDep
from src.database import async_session_maker

from src.schemas.hotels import HotelPOST, HotelPUT, HotelPATCH
from src.models.hotels import HotelsOrm
from src.assets.openapi_examples.hotels import (
    POST_OPENAPI_EXAMPLE,
    PUT_OPENAPI_EXAMPLE,
    PATCH_OPENAPI_EXAMPLE,
)

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/hotels", summary="Получить список отелей")
async def get_hotels(
    pagination: PaginationDep,
    title: str = Query(default=None, description="Название отеля"),
    location: int = Query(default=None, description="Адрес"),
):
    async with async_session_maker() as session:
        query = select(HotelsOrm)

        if title:
            query = query.filter_by(title=title)

        query = query.limit(pagination.per_page).offset(
            pagination.per_page * (pagination.page - 1)
        )

        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels

    # start = (pagination.page - 1) * pagination.per_page
    # end = start + pagination.per_page


@router.get("/hotels/{id}", summary="Получить информацию по отелю")
def get_hotel(id: int = Path(description="ИД отеля")):
    for hotel in hotels:
        if hotel["id"] == id:
            return hotel


@router.post("/hotels", summary="Создать отель")
async def create_hotel(
    hotel_data: HotelPOST = Body(openapi_examples=POST_OPENAPI_EXAMPLE),
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()
    return hotel_data.model_dump()


@router.put("/hotels/{id}", summary="Обновить все поля отеля")
def update_hotel(
    id: int = Path(description="ИД отеля"),
    hotel_data: HotelPUT = Body(openapi_examples=PUT_OPENAPI_EXAMPLE),
):
    hotel = [hotel for hotel in hotels if hotel["id"] == id][0]
    hotel["title"] = hotel_data.title
    hotel["stars"] = hotel_data.stars

    return hotel


@router.patch("/hotels/{id}", summary="Обновить выбранные поля отеля")
def edit_hotel(
    id: int = Path(description="ИД отеля"),
    hotel_data: HotelPATCH = Body(openapi_examples=PATCH_OPENAPI_EXAMPLE),
):
    hotel = [hotel for hotel in hotels if hotel["id"] == id][0]
    hotel["title"] = hotel_data.title if hotel_data.title else hotel["title"]
    hotel["stars"] = hotel_data.stars if hotel_data.stars else hotel["stars"]

    return hotel


@router.delete("/hotels/{id}", summary="Удалить отель")
def delete_hotels(id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != id]
    return {"status": "OK"}
