from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.schemas.bookings import BookingSchema


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = BookingSchema