from app.api.schemas.users import UserDBSchema
from app.db.crud.mappers.base import DataMapper
from app.db.models import Users


class UsersMapper(DataMapper):
    model = Users
    schema = UserDBSchema
