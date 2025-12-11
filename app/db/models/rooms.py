from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base

class Rooms(Base):
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'))