from sqlalchemy import select

from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import HotelDataMapper

from src.models.rooms import RoomsOrm
from src.repositories.utils import get_rooms_by_date

class HotelsRepository(BaseRepository):
    model = HotelsOrm
    mapper = HotelDataMapper

    async def get_all(self, title, location, date_from, date_to, limit, offset):
        query = select(self.model)

        if title:
            query = query.filter(self.model.title.ilike(f"%{title}%"))
        if location:
            query = query.filter(self.model.location.ilike(f"%{location}%"))

        if date_from or date_to:
            query_get_rooms = get_rooms_by_date(date_from=date_from, date_to=date_to)
            rooms = await self.session.execute(query_get_rooms)
            query_get_hotels = (
                select(RoomsOrm.hotel_id)
                .select_from(RoomsOrm)
                .filter(RoomsOrm.id.in_(rooms.scalars().all()))
            )
            hotels = await self.session.execute(query_get_hotels)
            query = query.filter(self.model.id.in_(hotels.scalars().all()))

        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)

        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]
