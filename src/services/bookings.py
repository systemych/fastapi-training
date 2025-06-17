from src.services.base import BaseService
from src.schemas.bookings import BookingAdd, BookingInsert, BookingUpdate
from src.exeptions import DataValidationExeption, NotFoundExeption, UnavailableExeption

class BookingService(BaseService):
    async def create_booking(self, user_id: int, booking_data: BookingAdd):
        date_from = booking_data.date_from
        date_to = booking_data.date_to

        if date_from is not None and date_to is not None:
            if date_to <= date_from:
                raise DataValidationExeption()

        room = await self.db.rooms.get_one_or_none(id=booking_data.room_id)
        if room is None:
            raise NotFoundExeption()

        hotel_id = room.hotel_id
        hotel_rooms_on_date = await self.db.rooms.get_all(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to,
        )

        room_is_available = (
            len(list(filter(lambda r: r.id == booking_data.room_id, hotel_rooms_on_date)))
            > 0
        )

        if not room_is_available:
            raise UnavailableExeption(detail="Room is not available on date period")

        result = await self.db.bookings.add(
            BookingInsert(user_id=user_id, price=room.price, **booking_data.model_dump())
        )

        await self.db.commit()
        return result

    async def get_bookings(self):
        result = await self.db.bookings.get_all()
        return result

    async def get_my_bookings(self, user_id:int):
        result = await self.db.bookings.get_all(user_id=user_id)
        return result

    async def update_booking(
        self,
        id: int,
        user_id: int,
        booking_data: BookingUpdate,
    ):
        date_from = booking_data.date_from
        date_to = booking_data.date_to

        if date_from is not None and date_to is not None:
            if date_to <= date_from:
                raise DataValidationExeption()

        room = await self.db.rooms.get_one_or_none(id=booking_data.room_id)
        if room is None:
            raise NotFoundExeption()

        result = await self.db.bookings.update(
            BookingInsert(user_id=user_id, price=room.price, **booking_data.model_dump()),
            id=id,
        )
        await self.db.commit()
        return result

    async def delete_booking(
        self,
        id: int
    ):
        booking = await self.db.rooms.get_one_or_none(id=id)
        if not booking:
            raise NotFoundExeption()

        await self.db.bookings.delete(id=id)
        await self.db.commit()