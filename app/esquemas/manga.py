from pydantic import BaseModel, Field
from uuid import UUID
from pydantic import BaseModel
from enum import Enum


class MangaCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255
    )

    description: str | None = Field(
        default=None,
        max_length=5000
    )

    cover_url: str | None = None

class MangaStatus(str, Enum):
    draft = "draft"
    published = "published"
    archived = "archived"

class MangaUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    cover_url: str | None = None
    status: MangaStatus | None = None

class MangaOut(BaseModel):
    id: UUID
    author_id: UUID

    title: str
    description: str | None = None
    cover_url: str | None = None
    status: str

    class Config:
        from_attributes = True

