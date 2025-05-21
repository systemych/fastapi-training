from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import RoomSchema, RoomWithOptionsSchema
from src.repositories.utils import get_rooms_by_date


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = RoomSchema

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
                RoomWithOptionsSchema.model_validate(model, from_attributes=True)
                for model in result
            ]

        query = select(self.model).options(selectinload(self.model.options))

        if hotel_id:
            query = query.filter_by(hotel_id=hotel_id)

        result = await self.session.execute(query)
        return [
            RoomWithOptionsSchema.model_validate(model, from_attributes=True)
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

        return RoomWithOptionsSchema.model_validate(model, from_attributes=True)
