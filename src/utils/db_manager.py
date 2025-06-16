from src.repositories.hotels import HotelsRepository
from src.repositories.rooms import RoomsRepository
from src.repositories.users import UsersRepository
from src.repositories.bookings import BookingsRepository
from src.repositories.options import OptionsRepository, RoomsOptionsRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.sesion = self.session_factory()

        self.hotels = HotelsRepository(self.sesion)
        self.rooms = RoomsRepository(self.sesion)
        self.users = UsersRepository(self.sesion)
        self.bookings = BookingsRepository(self.sesion)
        self.options = OptionsRepository(self.sesion)
        self.rooms_options = RoomsOptionsRepository(self.sesion)

        return self

    async def __aexit__(self, *args):
        await self.sesion.rollback()
        await self.sesion.close()

    async def commit(self):
        await self.sesion.commit()

    async def flush(self):
        await self.sesion.flush()
