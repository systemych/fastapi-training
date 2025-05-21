from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils import get_rooms_by_date
from src.repositories.mappers.mappers import RoomWithOptionsDataMapper


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomWithOptionsDataMapper

    async def get_all(self, hotel_id, date_from, date_to):
        # не нравится, как реализовано, в техдолг
        if date_from or date_to:
            query_get_rooms_by_date = get_rooms_by_date(
                hotel_id=hotel_id, date_from=date_from, date_to=date_to
            )

            rooms_by_date = await self.session.execute(query_get_rooms_by_date)
            result = []
            for room_orm, new_quantity in rooms_by_date.all():
                room_orm.quantity = new_quantity
                result.append(room_orm)

            return [
                self.mapper.map_to_domain_entity(model)
                for model in result
            ]

        query = select(self.model).options(selectinload(self.model.options))

        if hotel_id:
            query = query.filter_by(hotel_id=hotel_id)

        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(model)
            for model in result.scalars().all()
        ]

    async def get_one_or_none(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.options))
            .filter_by(**filter_by)
        )

        result = await self.session.execute(query)
        model = result.scalars().one_or_none()

        if model is None:
            return None

        return self.mapper.map_to_domain_entity(model)
