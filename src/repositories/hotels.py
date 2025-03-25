from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(self, title, location, limit, offset):
        query = select(self.model)
        result = await self.session.execute(query)

        if title:
            query = query.filter(self.model.title.ilike(f"%{title}%"))
        if location:
            query = query.filter(self.model.location.ilike(f"%{location}%"))

        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return result.scalars().all()
