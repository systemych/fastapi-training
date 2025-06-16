from datetime import date

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from src.models.rooms import RoomsOrm
from src.models.bookings import BookingsOrm


def get_rooms_by_date(
    date_from: date,
    date_to: date,
    hotel_id: int | None = None,
):
    cte_rooms_booked = (
        select(BookingsOrm.room_id, func.count("*").label("count"))
        .select_from(BookingsOrm)
        .group_by(BookingsOrm.room_id)
    )

    if date_from and date_to:
        cte_rooms_booked = cte_rooms_booked.filter(
            BookingsOrm.date_from < date_to, BookingsOrm.date_to > date_from
        )
    elif date_from:
        cte_rooms_booked = cte_rooms_booked.filter(BookingsOrm.date_to > date_from)
    elif date_to:
        cte_rooms_booked = cte_rooms_booked.filter(BookingsOrm.date_from < date_to)

    cte_rooms_booked = cte_rooms_booked.cte(name="cte_rooms_booked")

    cte_rooms_left = (
        select(
            RoomsOrm.id,
            (RoomsOrm.quantity - func.coalesce(cte_rooms_booked.c.count, 0)).label("rooms_left"),
        )
        .select_from(RoomsOrm)
        .outerjoin(cte_rooms_booked, RoomsOrm.id == cte_rooms_booked.c.room_id)
        .cte(name="cte_rooms_left")
    )

    if hotel_id:
        rooms_ids_by_hotel_id = (
            select(RoomsOrm.id).select_from(RoomsOrm).filter(RoomsOrm.hotel_id == hotel_id)
        )

        query_filter = [
            cte_rooms_left.c.rooms_left > 0,
            cte_rooms_left.c.id.in_(rooms_ids_by_hotel_id),
        ]
    else:
        query_filter = [cte_rooms_left.c.rooms_left > 0]

    query = (
        select(RoomsOrm)
        .join(cte_rooms_left, RoomsOrm.id == cte_rooms_left.c.id)
        .filter(*query_filter)
        .options(selectinload(RoomsOrm.options))
        .add_columns(cte_rooms_left.c.rooms_left.label("quantity"))
    )

    return query
