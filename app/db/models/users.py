from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Users(Base):
    email: Mapped[str] = mapped_column(String(200), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(200))

    image_id: Mapped[int] = mapped_column(ForeignKey('images.id'), nullable=True)