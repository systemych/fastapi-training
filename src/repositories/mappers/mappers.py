from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm
from src.models.bookings import BookingsOrm
from src.models.options import OptionsOrm, RoomsOptionsOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.hotels import HotelSchema
from src.schemas.rooms import RoomSchema, RoomWithOptionsSchema
from src.schemas.users import UserSchemaWithHashedPassword
from src.schemas.bookings import BookingSchema
from src.schemas.options import OptionSchema, RoomOptionSchema


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = HotelSchema


class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomSchema


class RoomWithOptionsDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomWithOptionsSchema


class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = UserSchemaWithHashedPassword


class BookingDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = BookingSchema


class OptionDataMapper(DataMapper):
    db_model = OptionsOrm
    schema = OptionSchema


class RoomOptionsDataMapper(DataMapper):
    db_model = RoomsOptionsOrm
    schema = RoomOptionSchema
