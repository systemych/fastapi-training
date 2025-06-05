from pydantic import EmailStr
from sqlalchemy import select

from src.models.users import UsersOrm
from src.schemas.users import UserSchemaWithHashedPassword
from src.repositories.base import BaseRepository

class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = UserSchemaWithHashedPassword

    async def get_user_with_hashed_password(self, email:EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return self.map_to_domain_entity(model)