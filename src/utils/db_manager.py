from src.repositories.hotels import HotelsRepository
from src.repositories.rooms import RoomsRepository
from src.repositories.users import UsersRepository


class DBManager():
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.sesion = self.session_factory()

        self.hotels = HotelsRepository(self.sesion)
        self.rooms = RoomsRepository(self.sesion)
        self.users = UsersRepository(self.sesion)

        return self

    async def __aexit__(self, *args):
        await self.sesion.rollback()
        await self.sesion.close()

    async def commit(self):
        await self.sesion.commit()