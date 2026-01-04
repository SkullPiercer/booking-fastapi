from sqlalchemy import Integer, NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base, declared_attr, Mapped, mapped_column

from app.core.config import get_settings

settings = get_settings()


class PreBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

params = {}
if settings.MODE == 'test':
    params = {'poolclass': NullPool}

engine = create_async_engine(settings.DB_URL, **params)
engine_null_pool = create_async_engine(settings.DB_URL, poolclass=NullPool)

Base = declarative_base(cls=PreBase)

async_session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async_session_maker_null_pool = async_sessionmaker(
    bind=engine_null_pool,
    expire_on_commit=False
)
