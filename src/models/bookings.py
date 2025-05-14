import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from src.database import Base

class BookingsOrm(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[datetime.datetime]
    date_to: Mapped[datetime.datetime]
    price: Mapped[int]