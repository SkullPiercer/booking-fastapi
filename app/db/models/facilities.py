from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Facilities(Base):
    title: Mapped[str] = mapped_column(String(100))

    rooms: Mapped[list['Rooms']] = relationship(
        back_populates='facilities',
        secondary='roomsfacilities',
    )


class RoomsFacilities(Base):
    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'))
    facility_id: Mapped[int] = mapped_column(ForeignKey('facilities.id'))
