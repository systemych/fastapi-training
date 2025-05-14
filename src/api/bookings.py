from fastapi import APIRouter, HTTPException, status
from src.api.dependencies import UserIdDep, DBDep
from src.schemas.bookings import BookingAdd, BookingInsert

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("/", summary="Забронировать номер в отеле")
async def create_booking(db: DBDep, user_id: UserIdDep, booking_data: BookingAdd):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    result = await db.bookings.add(
        BookingInsert(
            user_id=user_id,
            price=room.price,
            **booking_data.model_dump()
        )
    )
    await db.commit()
    return result
