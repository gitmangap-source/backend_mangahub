from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.database import Base


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    manga_id = Column(
        UUID(as_uuid=True),
        ForeignKey("mangas.id", ondelete="CASCADE"),
        nullable=False
    )

    title = Column(
        String(255),
        nullable=False
    )

    chapter_number = Column(
        Integer,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    manga = relationship(
        "Manga",
        back_populates="chapters"
    )

    pages = relationship(
        "Page",
        back_populates="chapter",
        cascade="all, delete-orphan"
    )