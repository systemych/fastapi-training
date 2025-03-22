from pydantic import BaseModel, Field

class HotelPOST(BaseModel):
    title: str = Field(description="Название отеля")
    location: str = Field(description="Адрес")

class HotelPUT(BaseModel):
    title: str = Field(description="Название отеля")
    location: str = Field(description="Адрес")

class HotelPATCH(BaseModel):
    title: str | None = Field(default=None, description="Название отеля")
    location: str | None = Field(default=None, description="Адрес")