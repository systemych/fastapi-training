from fastapi import APIRouter, HTTPException, status, Path
from src.api.dependencies.user_id import UserIdDep
from src.api.dependencies.db_manager import DBDep
from src.schemas.bookings import BookingAdd, BookingUpdate
from src.services.bookings import BookingService
from src.exeptions import DataValidationExeption, NotFoundExeption, UnavailableExeption

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("/", summary="Забронировать номер в отеле")
async def create_booking(db: DBDep, user_id: UserIdDep, booking_data: BookingAdd):
    try:
        result = await BookingService(db).create_booking(user_id, booking_data)
    except DataValidationExeption as ex:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=ex.detail,
        )
    except NotFoundExeption as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.detail)
    except UnavailableExeption as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ex.detail,
        )

    return result


@router.get("/", summary="Получить все бронирования")
async def get_bookings(db: DBDep, user_id: UserIdDep):
    result = await BookingService(db).get_bookings()
    return result


@router.get("/me", summary="Получить все свои бронирования")
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    result = await BookingService(db).get_my_bookings(user_id)
    return result


@router.put("/{id}", summary="Обновить бронирование")
async def update_booking(
    db: DBDep,
    user_id: UserIdDep,
    booking_data: BookingUpdate,
    id: int = Path(description="ИД бронирования"),
):
    try:
        result = await BookingService(db).update_booking(id, user_id, booking_data)
    except DataValidationExeption as ex:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=ex.detail,
        )
    except NotFoundExeption as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.detail,
        )

    return result


@router.delete("/{id}", summary="Удалить бронирование")
async def delete_booking(
    db: DBDep,
    user_id: UserIdDep,
    id: int = Path(description="ИД бронирования"),
):
    try:
        await BookingService(db).delete_booking(id)
    except NotFoundExeption as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.detail)

    return "OK"
