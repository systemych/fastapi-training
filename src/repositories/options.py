from sqlalchemy import delete

from src.repositories.base import BaseRepository
from src.models.options import OptionsOrm, RoomsOptionsOrm
from src.schemas.options import OptionSchema, RoomOptionSchema


class OptionsRepository(BaseRepository):
    model = OptionsOrm
    schema = OptionSchema

class RoomsOptionsRepository(BaseRepository):
    model = RoomsOptionsOrm
    schema = RoomOptionSchema

    async def delete_bulk_by_option_id(self, ids):
        delete_hotel_stmt = delete(self.model).filter(self.model.option_id.in_(ids))
        await self.session.execute(delete_hotel_stmt)