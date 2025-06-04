from sqlalchemy import delete

from src.models.options import OptionsOrm, RoomsOptionsOrm
from src.repositories.base import BaseRepository
from src.schemas.options import OptionSchema, RoomOptionSchema, RoomsOptionsAdd


class OptionsRepository(BaseRepository):
    model = OptionsOrm
    schema = OptionSchema

class RoomsOptionsRepository(BaseRepository):
    model = RoomsOptionsOrm
    schema = RoomOptionSchema

    async def delete_bulk_by_option_id(self, ids):
        delete_stmt = delete(self.model).filter(self.model.option_id.in_(ids))
        await self.session.execute(delete_stmt)

    async def update(self, room_id, options_ids: list[int]):
        current_room_options = await self.get_all(room_id=room_id)
        current_room_options_ids = [room_option.option_id for room_option in current_room_options]

        options_to_add = list(set(options_ids) - set(current_room_options_ids))
        options_to_delete = list(set(current_room_options_ids) - set(options_ids))

        if len(options_to_add) > 0:
            await self.add_bulk([RoomsOptionsAdd(room_id=room_id, option_id=o_id) for o_id in options_to_add])
        if len(options_to_delete) > 0:
            await self.delete_bulk_by_option_id(options_to_delete)