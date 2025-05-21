from pydantic import BaseModel, Field
from src.schemas.options import OptionSchema

class RoomSchema(BaseModel):
    id: int
    hotel_id: int
    title: str
    description: str | None
    price: int
    quantity: int

class RoomWithOptionsSchema(RoomSchema):
    options: list[OptionSchema] | None

class RoomAddRequest(BaseModel):
    hotel_id: int = Field(description="ИД отеля")
    title: str = Field(description="Название")
    description: str | None = Field(default=None, description="Описание")
    price: int = Field(description="Стоимость")
    quantity: int = Field(description="Количество")
    options_ids: list[int] | None = Field(default=None, description="ИД добавляемых опций номера")

class RoomAddSchema(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int

class RoomUpdateRequest(BaseModel):
    title: str = Field(description="Название")
    description: str | None = Field(default=None, description="Описание")
    price: int = Field(description="Стоимость")
    quantity: int = Field(description="Количество")
    options_ids: list[int] | None = Field(default=None, description="ИД добавляемых опций номера")

class RoomUpdateSchema(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int

class RoomEditRequest(BaseModel):
    title: str | None = Field(default=None, description="Название")
    description: str | None = Field(default=None, description="Описание")
    price: int | None = Field(default=None, description="Стоимость")
    quantity: int | None = Field(default=None, description="Количество")
    options_ids: list[int] | None = Field(default=None, description="ИД добавляемых опций номера")

class RoomEditSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None

class RoomResponse(BaseModel):
    id: int = Field(description="ИД номера")
    hotel_id: int = Field(description="ИД отеля")
    title: str = Field(description="Название")
    description: str | None = Field(default=None, description="Описание")
    price: int = Field(description="Стоимость")
    quantity: int = Field(description="Количество")
    options: list[OptionSchema] | None = Field(default=None, description="Опции номера")