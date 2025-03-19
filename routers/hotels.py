from fastapi import Query, Path, Body, APIRouter, Depends
from schemas.hotels import HotelPOST, HotelPUT, HotelPATCH
from dependencies import PaginationDep
from assets.openapi_examples.hotels import (
    POST_OPENAPI_EXAMPLE,
    PUT_OPENAPI_EXAMPLE,
    PATCH_OPENAPI_EXAMPLE,
)

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Сочи", "stars": 4},
    {"id": 2, "title": "Дубаи", "stars": 4},
    {"id": 3, "title": "Мальдивы", "stars": 5},
    {"id": 4, "title": "Геленджик", "stars": 3},
    {"id": 5, "title": "Москва", "stars": 3},
    {"id": 6, "title": "Казань", "stars": 3},
    {"id": 7, "title": "Санкт-Петербург", "stars": 4},
]


@router.get("/hotels", summary="Получить список отелей")
def get_hotels(
    pagination: PaginationDep,
    title: str = Query(default=None, description="Название отеля"),
    stars: int = Query(default=None, description="Количество звёзд"),
):
    result = []
    for hotel in hotels:
        if title and hotel["title"] != title:
            continue
        if stars and hotel["stars"] != stars:
            continue
        result.append(hotel)

    start = (pagination.page - 1) * pagination.per_page
    end = start + pagination.per_page

    return result[start:end]


@router.get("/hotels/{id}", summary="Получить информацию по отелю")
def get_hotel(id: int = Path(description="ИД отеля")):
    for hotel in hotels:
        if hotel["id"] == id:
            return hotel


@router.post("/hotels", summary="Создать отель")
def create_hotel(hotel_data: HotelPOST = Body(openapi_examples=POST_OPENAPI_EXAMPLE)):
    hotel = {
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "stars": hotel_data.stars,
    }
    hotels.append(hotel)

    return hotel


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
