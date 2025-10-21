from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Hotels(Base):
    title: Mapped[str] = mapped_column(String(100))
    location: Mapped[str]