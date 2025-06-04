from pydantic import BaseModel
from sqlalchemy import select, insert, update
from sqlalchemy.orm import selectinload

from src.models.rooms import RoomsOrm
from src.schemas.rooms import RoomWithOptionsSchema
from src.repositories.base import BaseRepository
from src.repositories.utils import get_rooms_by_date


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = RoomWithOptionsSchema

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
                self.map_to_domain_entity(model)
                for model in result
            ]

        query = select(self.model).options(selectinload(self.model.options))

        if hotel_id:
            query = query.filter_by(hotel_id=hotel_id)

        result = await self.session.execute(query)
        return [
            self.map_to_domain_entity(model)
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

        return self.map_to_domain_entity(model)


    async def add(self, data: BaseModel):
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model.id)
        result = await self.session.execute(add_stmt)
        return result.scalars().one()


    async def update(self, data: BaseModel, exсlude_unset: bool = False, **filter_by):
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exсlude_unset))
        )
        await self.session.execute(update_stmt)


    async def edit(self, data: BaseModel, exсlude_unset: bool = False, **filter_by):
        if not data.model_dump(exclude_unset=exсlude_unset):
            return await self.get_one_or_none(**filter_by)

        edit_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exсlude_unset))
        )

        await self.session.execute(edit_stmt)