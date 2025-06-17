import jwt
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status

from src.services.base import BaseService
from src.config import settings
from src.schemas.users import UserRegister, UserAdd
from src.exeptions import AlreadyExistsExeption, NotFoundExeption, BadCredentialsExeption


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен")

    async def register_user(
        self,
        data: UserRegister,
    ):
        hashed_password = self.hash_password(data.password)
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
        user_with_same_email = await self.db.users.get_one_or_none(email=data.email)
        if user_with_same_email:
            raise AlreadyExistsExeption()
        result = await self.db.users.add(new_user_data)
        await self.db.commit()
        return result

    async def login_user(
        self,
        data: UserRegister
    ):
        user = await self.db.users.get_user_with_hashed_password(email=data.email)
        if not user:
            raise NotFoundExeption()
        if not self.verify_password(data.password, user.hashed_password):
            raise BadCredentialsExeption()

        access_token = self.create_access_token({"user_id": user.id})

        return access_token

    async def get_me(self, user_id: int):
        user = await self.db.users.get_one_or_none(id=user_id)
        return user
