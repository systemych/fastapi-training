from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import RoomSchema
from src.repositories.utils import get_rooms_by_date


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = RoomSchema

    async def get_all(self, hotel_id, date_from, date_to):
        # не нравится, как реализовано, в техдолг
        if date_from or date_to:
            query_get_rooms = get_rooms_by_date(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
            result = await self.session.execute(query_get_rooms)

            return [
                self.schema.model_validate(model, from_attributes=True)
                for model in result.all()
            ]

        query = select(self.model)

        if hotel_id:
            query = query.filter_by(hotel_id=hotel_id)

        result = await self.session.execute(query)
        return [
            self.schema.model_validate(model, from_attributes=True)
            for model in result.scalars().all()
        ]