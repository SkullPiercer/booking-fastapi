from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

class Images(Base):
    file_path: Mapped[str | None] = mapped_column(None, String(100), unique=True)
