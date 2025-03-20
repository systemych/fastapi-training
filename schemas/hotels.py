from pydantic import BaseModel, Field

class HotelPOST(BaseModel):
    title: str = Field(description="Название отеля")
    stars: int = Field(description="Количество звёзд")

class HotelPUT(BaseModel):
    title: str = Field(description="Название отеля")
    stars: int = Field(description="Количество звёзд")

class HotelPATCH(BaseModel):
    title: str | None = Field(default=None, description="Название отеля")
    stars: int | None = Field(default=None, description="Количество звёзд")