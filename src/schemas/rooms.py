from pydantic import BaseModel, Field

class RoomSchema(BaseModel):
    id: int
    hotel_id: int
    title: str
    description: str | None
    price: int
    quantity: int

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
    title: str | None
    description: str | None
    price: int | None
    quantity: int | None

class RoomResponse(BaseModel):
    id: int = Field(description="ИД номера")
    hotel_id: int = Field(description="ИД отеля")
    title: str = Field(description="Название")
    description: str | None = Field(default=None, description="Описание")
    price: int = Field(description="Стоимость")
    quantity: int = Field(description="Количество")
    options_ids: list[int] | None = Field(default=None, description="ИД опций номера")