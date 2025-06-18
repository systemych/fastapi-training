from datetime import date

from src.services.base import BaseService
from src.api.dependencies.pagination import PaginationDep
from src.schemas.hotels import HotelAdd, HotelUpdate, HotelEdit
from src.exeptions import DataValidationExeption, NotFoundExeption


class HotelService(BaseService):
    async def get_hotels(
        self,
        pagination: PaginationDep,
        title: str,
        location: str,
        date_from: date,
        date_to: date,
    ):
        if date_from is not None and date_to is not None:
            if date_to <= date_from:
                raise DataValidationExeption()

        result = await self.db.hotels.get_all(
            title=title,
            location=location,
            date_from=date_from,
            date_to=date_to,
            limit=pagination.per_page,
            offset=pagination.per_page * (pagination.page - 1),
        )

        return result

    async def get_hotel(self, id: int):
        requested_hotel = await self.db.hotels.get_one_or_none(id=id)

        if requested_hotel is None:
            raise NotFoundExeption()

        return requested_hotel

    async def create_hotel(self, hotel_data: HotelAdd):
        result = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return result

    async def update_hotel(self, id: int, hotel_data: HotelUpdate):
        requested_hotel = await self.db.hotels.get_one_or_none(id=id)

        if requested_hotel is None:
            raise NotFoundExeption()

        result = await self.db.hotels.update(hotel_data, id=id)
        await self.db.commit()
        return result

    async def edit_hotel(
        self,
        id: int,
        hotel_data: HotelEdit,
    ):
        requested_hotel = await self.db.hotels.get_one_or_none(id=id)

        if requested_hotel is None:
            raise NotFoundExeption()

        result = await self.db.hotels.edit(hotel_data, exсlude_unset=True, id=id)
        await self.db.commit()
        return result

    async def delete_hotels(self, id: int):
        requested_hotel = await self.db.hotels.get_one_or_none(id=id)

        if requested_hotel is None:
            raise NotFoundExeption()

        await self.db.hotels.delete(id=id)
        await self.db.commit()