from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    id: int
    email: EmailStr

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str
