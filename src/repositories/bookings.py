from datetime import date
from sqlalchemy import select, delete

from src.models.bookings import BookingsOrm
from src.schemas.bookings import BookingSchema
from src.repositories.base import BaseRepository

class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = BookingSchema

    async def get_bookings_with_today_checkin(self):
        query = (
            select(BookingsOrm)
            .filter(BookingsOrm.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.map_to_domain_entity(booking) for booking in res.scalars().all()]