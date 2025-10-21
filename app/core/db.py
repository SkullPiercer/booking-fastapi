from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, Mapped, mapped_column

from app.core.config import get_settings

settings = get_settings()


class PreBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() # type: ignore

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

engine = create_async_engine(settings.DB_URL)

Base = declarative_base(cls=PreBase)
