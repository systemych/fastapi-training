from fastapi import APIRouter, HTTPException, status, Path
from src.api.dependencies import UserIdDep, DBDep
from src.schemas.bookings import BookingAdd, BookingInsert, BookingUpdate

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("/", summary="Забронировать номер в отеле")
async def create_booking(db: DBDep, user_id: UserIdDep, booking_data: BookingAdd):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    result = await db.bookings.add(
        BookingInsert(user_id=user_id, price=room.price, **booking_data.model_dump())
    )
    await db.commit()
    return result


@router.get("/", summary="Получить все бронирования")
async def get_bookings(db: DBDep, user_id: UserIdDep):
    result = await db.bookings.get_all()
    return result


@router.get("/me", summary="Получить все свои бронирования")
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    result = await db.bookings.get_all(user_id=user_id)
    return result


@router.put("/{id}", summary="Обновить бронирование")
async def update_booking(
    db: DBDep,
    user_id: UserIdDep,
    booking_data: BookingUpdate,
    id: int = Path(description="ИД бронирования"),
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    result = await db.bookings.update(
        BookingInsert(user_id=user_id, price=room.price, **booking_data.model_dump()),
        id=id,
    )
    await db.commit()
    return result


@router.delete("/{id}", summary="Удалить бронирование")
async def delete_booking(
    db: DBDep,
    user_id: UserIdDep,
    id: int = Path(description="ИД бронирования"),
):
    booking = await db.rooms.get_one_or_none(id=id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    await db.bookings.delete(id=id)
    await db.commit()
    return "OK"
