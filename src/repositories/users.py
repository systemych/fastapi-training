from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.schemas.users import UserSchema

class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = UserSchema