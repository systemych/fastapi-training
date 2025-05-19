from pydantic import BaseModel, Field

class OptionSchema(BaseModel):
    id: int
    title: str

class OptionAdd(BaseModel):
    title: str = Field(description="Название")

class OptionUpdate(BaseModel):
    title: str = Field(description="Название")