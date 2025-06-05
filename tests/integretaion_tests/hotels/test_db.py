from src.schemas.hotels import HotelAdd

async def test_add_hotel(db):
    hotel_data = HotelAdd(title="Жига-Дрыга", location="Серпухов")
    await db.hotels.add(hotel_data)
    await db.commit()