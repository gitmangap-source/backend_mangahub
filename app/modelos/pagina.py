from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.db.database import Base


class Page(Base):
    __tablename__ = "pages"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    chapter_id = Column(
        UUID(as_uuid=True),
        ForeignKey("chapters.id", ondelete="CASCADE"),
        nullable=False
    )

    image_url = Column(
        String(500),
        nullable=False
    )

    page_number = Column(
        Integer,
        nullable=False
    )

    chapter = relationship(
        "Chapter",
        back_populates="pages"
    )