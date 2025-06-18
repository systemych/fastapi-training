from datetime import date

from src.services.base import BaseService
from src.schemas.options import OptionAdd, OptionUpdate
from src.tasks.tasks import test_task
from src.exeptions import NotFoundExeption, AlreadyExistsExeption

class OptionService(BaseService):
    async def create_option(self, option_data: OptionAdd):
        option = await self.db.options.get_one_or_none(title=option_data.title)
        if option:
            raise AlreadyExistsExeption()

        result = await self.db.options.add(option_data)
        await self.db.commit()

        return result

    async def get_options(self):
        test_task.delay()
        return await self.db.options.get_all()

    async def update_option(
        self,
        option_data: OptionUpdate,
        id: int,
    ):
        option = await self.db.options.get_one_or_none(id=id)
        if option is None:
            raise NotFoundExeption()

        result = await self.db.options.update(option_data, id=id)
        return result
