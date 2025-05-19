from src.repositories.base import BaseRepository
from src.models.options import OptionsOrm
from src.schemas.options import OptionSchema


class OptionsRepository(BaseRepository):
    model = OptionsOrm
    schema = OptionSchema