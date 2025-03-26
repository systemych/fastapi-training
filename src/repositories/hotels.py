from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from src.schemas.hotels import HotelSchema


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = HotelSchema

    async def get_all(self, title, location, limit, offset):
        query = select(self.model)
        result = await self.session.execute(query)

        if title:
            query = query.filter(self.model.title.ilike(f"%{title}%"))
        if location:
            query = query.filter(self.model.location.ilike(f"%{location}%"))

        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
