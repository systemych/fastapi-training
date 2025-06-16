from pydantic import BaseModel, Field


class HotelSchema(BaseModel):
    id: int
    title: str
    location: str


class HotelAdd(BaseModel):
    title: str = Field(description="Название")
    location: str = Field(description="Адрес")


class HotelUpdate(BaseModel):
    title: str = Field(description="Название")
    location: str = Field(description="Адрес")


class HotelEdit(BaseModel):
    title: str | None = Field(default=None, description="Название")
    location: str | None = Field(default=None, description="Адрес")
