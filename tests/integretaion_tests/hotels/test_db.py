from src.database import async_session_maker_null_pool
from src.utils.db_manager import DBManager
from src.schemas.hotels import HotelAdd

async def test_add_hotel():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        hotel_data = HotelAdd(title="Жига-Дрыга", location="Серпухов")
        await db.hotels.add(hotel_data)
        await db.commit()