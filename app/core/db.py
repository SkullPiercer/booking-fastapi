from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
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

async_session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_async_session():
    async with async_session_maker() as async_session:
        yield async_session
