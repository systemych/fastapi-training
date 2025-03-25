from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete

class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_stmt)
        return result.scalars().one()

    async def update(self, data: BaseModel, **filter_by):
        update_hotel_stmt = (
            update(self.model).filter_by(**filter_by).values(**data.model_dump()).returning(self.model)
        )
        result = await self.session.execute(update_hotel_stmt)
        return result.scalars().one()

    async def delete(self, **filter_by):
        delete_hotel_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_hotel_stmt)