from src.repositories.base import BaseRepository
from src.models.options import OptionsOrm, RoomsOptionsOrm
from src.schemas.options import OptionSchema, RoomOptionSchema


class OptionsRepository(BaseRepository):
    model = OptionsOrm
    schema = OptionSchema

class RoomsOptionsRepository(BaseRepository):
    model = RoomsOptionsOrm
    schema = RoomOptionSchema