from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)

        models = result.scalars().all()
        print(models)
        return [
            self.schema.model_validate(model, from_attributes=True)
            for model in models
        ]

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model, from_attributes=True)

    async def add(self, data: BaseModel):
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_stmt)
        model = result.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)

    async def add_bulk(self, data: list[BaseModel]):
        add_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_stmt)

    async def update(self, data: BaseModel, exсlude_unset: bool = False, **filter_by):
        update_hotel_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exсlude_unset))
            .returning(self.model)
        )
        result = await self.session.execute(update_hotel_stmt)
        model = result.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)

    async def edit(self, data: BaseModel, exсlude_unset: bool = False, **filter_by):
        edit_hotel_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exсlude_unset))
            .returning(self.model)
        )

        result = await self.session.execute(edit_hotel_stmt)
        model = result.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)

    async def delete(self, **filter_by):
        delete_hotel_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_hotel_stmt)
