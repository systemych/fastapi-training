from datetime import date
from pydantic import BaseModel, Field, ConfigDict

class BookingSchema(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int

class BookingAdd(BaseModel):
    room_id: int = Field(description="ИД команты")
    date_from: date = Field(description="Дата начала бронирования")
    date_to: date = Field(description="Дата окончания бронирования")

class BookingInsert(BookingAdd):
    user_id: int
    price: int

    model_config = ConfigDict(from_attributes=True)

class BookingUpdate(BookingAdd):
    ...