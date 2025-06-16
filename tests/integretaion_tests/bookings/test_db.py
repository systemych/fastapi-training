from datetime import date
from src.schemas.bookings import BookingInsert

async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id

    booking_data = BookingInsert(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2025, month=11, day=25),
        date_to=date(year=2025, month=11, day=30),
        price=3000
    )

    booking = await db.bookings.add(booking_data)
    await db.bookings.get_one_or_none(id=booking.id)
    await db.bookings.update(booking_data, id=booking.id)
    await db.bookings.delete(id=booking.id)

    await db.commit()