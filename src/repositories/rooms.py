from sqlalchemy import select, func

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.models.bookings import BookingsOrm
from src.schemas.rooms import RoomSchema

from database import engine


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = RoomSchema

    async def get_all_by_date(self, hotel_id, date_from, date_to):
        cte_rooms_booked = (
            select(BookingsOrm.room_id, func.count("*").label("count"))
            .select_from(BookingsOrm)
            .filter(BookingsOrm.date_from <= date_to, BookingsOrm.date_to >= date_from)
            .group_by(BookingsOrm.room_id)
            .cte(name="cte_rooms_booked")
        )

        cte_rooms_left = (
            select(
                RoomsOrm.id,
                (RoomsOrm.quantity - func.coalesce(cte_rooms_booked.c.count, 0)).label(
                    "rooms_left"
                ),
            )
            .select_from(RoomsOrm)
            .outerjoin(cte_rooms_booked, RoomsOrm.id == cte_rooms_booked.c.room_id)
            .cte(name="cte_rooms_left")
        )

        left_rooms_ids_in_hotel = (
            select(cte_rooms_left.c.id)
            .select_from(cte_rooms_left)
            .filter(
                cte_rooms_left.c.rooms_left > 0,
                cte_rooms_left.c.id.in_(
                    select(RoomsOrm.id)
                    .select_from(RoomsOrm)
                    .filter(RoomsOrm.hotel_id == hotel_id)
                ),
            )
        )

        return await self.get_all(RoomsOrm.id.in_(left_rooms_ids_in_hotel))
