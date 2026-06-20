from pydantic import BaseModel
from uuid import UUID


class ChapterCreate(BaseModel):
    title: str
    chapter_number: int


class ChapterOut(BaseModel):
    id: UUID
    manga_id: UUID
    title: str
    chapter_number: int

    class Config:
        from_attributes = True