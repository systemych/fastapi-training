from datetime import date

from src.services.base import BaseService
from src.schemas.rooms import (
    RoomAddRequest,
    RoomAddSchema,
    RoomUpdateRequest,
    RoomUpdateSchema,
    RoomEditRequest,
    RoomEditSchema,
    RoomResponse,
)
from src.schemas.options import RoomsOptionsAdd
from src.exeptions import DataValidationExeption, NotFoundExeption


class RoomService(BaseService):
    async def get_rooms(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        if date_from is not None and date_to is not None:
            if date_to <= date_from:
                raise DataValidationExeption()

        result = await self.db.rooms.get_all(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

        return result

    async def get_room(self, id: int):
        requested_room = await self.db.rooms.get_one_or_none(id=id)

        if requested_room is None:
            raise NotFoundExeption()

        return requested_room

    async def create_room(
        self,
        room_data: RoomAddRequest
    ):
        hotel = await self.db.hotels.get_one_or_none(id=room_data.hotel_id)
        if hotel is None:
            raise NotFoundExeption()

        _room_data = RoomAddSchema(**room_data.model_dump())
        room_id = await self.db.rooms.add(_room_data)
        await self.db.flush()
        room = await self.db.rooms.get_one_or_none(id=room_id)

        if room_data.options_ids:
            room_options = [
                RoomsOptionsAdd(room_id=room.id, option_id=o_id) for o_id in room_data.options_ids
            ]
            await self.db.rooms_options.add_bulk(room_options)
        await self.db.commit()

        result = RoomResponse(options_ids=room_data.options_ids, **room.model_dump(exclude_none=True))
        return result

    async def update_room(
        self,
        id: int,
        updated_room: RoomUpdateRequest,
    ):
        _updated_room = RoomUpdateSchema(**updated_room.model_dump())
        current_room = await self.db.rooms.get_one_or_none(id=id)

        if current_room is None:
            raise NotFoundExeption()

        await self.db.rooms_options.update(id, updated_room.options_ids)
        await self.db.rooms.update(_updated_room, id=id)
        await self.db.commit()

        room_options = await self.db.rooms_options.get_all(room_id=id)
        updated_room = await self.db.rooms.get_one_or_none(id=id)

        result = RoomResponse(
            options_ids=[item.option_id for item in room_options],
            **updated_room.model_dump(),
        )
        return result


    async def edit_room(
        self,
        id: int,
        edited_room: RoomEditRequest,
    ):
        _edited_room = RoomEditSchema(**edited_room.model_dump(exclude_unset=True))

        current_room = await self.db.rooms.get_one_or_none(id=id)
        if current_room is None:
            raise NotFoundExeption()

        if edited_room.options_ids:
            await self.db.rooms_options.update(id, edited_room.options_ids)

        await self.db.rooms.edit(_edited_room, exсlude_unset=True, id=id)
        await self.db.commit()

        room_options = await self.db.rooms_options.get_all(room_id=id)
        updated_room = await self.db.rooms.get_one_or_none(id=id)

        result = RoomResponse(
            options_ids=[item.option_id for item in room_options],
            **updated_room.model_dump(),
        )
        return result

    async def delete_room(self, id: int):
        requested_room = await self.db.rooms.get_one_or_none(id=id)

        if requested_room is None:
            raise NotFoundExeption()

        await self.db.rooms_options.delete_bulk_by_option_id(
            ids=[option.id for option in requested_room.options]
        )
        await self.db.rooms.delete(id=id)
        await self.db.commit()