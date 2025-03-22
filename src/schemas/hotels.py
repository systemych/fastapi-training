from pydantic import BaseModel, Field

class HotelPOST(BaseModel):
    title: str = Field(description="Название")
    location: str = Field(description="Адрес")

class HotelPUT(BaseModel):
    title: str = Field(description="Название")
    location: str = Field(description="Адрес")

class HotelPATCH(BaseModel):
    title: str | None = Field(default=None, description="Название")
    location: str | None = Field(default=None, description="Адрес")