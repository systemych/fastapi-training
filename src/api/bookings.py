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
            **{
                "room_id": booking_data.room_id,
                "user_id": user_id,
                "date_from": booking_data.date_from,
                "date_to": booking_data.date_to,
                "price": room.price,
            }
        )
    )
    await db.commit()
    return result
