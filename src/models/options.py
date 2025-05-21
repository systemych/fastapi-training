from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from src.database import Base


class OptionsOrm(Base):
    __tablename__ = "options"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(127))

    rooms: Mapped[list["RoomsOrm"]] = relationship(
        back_populates="options",
        secondary="rooms_options"
    )

class RoomsOptionsOrm(Base):
    __tablename__ = "rooms_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey(column="rooms.id", name="rooms_options_room_id_idx"))
    option_id: Mapped[int] = mapped_column(ForeignKey(column="options.id", name="rooms_options_option_id_idx"))
