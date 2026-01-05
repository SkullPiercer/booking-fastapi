import typing

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


if typing.TYPE_CHECKING:
    from app.db.models import Facilities


class Rooms(Base):
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'))

    facilities: Mapped[list['Facilities']] = relationship(
        back_populates='rooms',
        secondary='roomsfacilities',
    )
