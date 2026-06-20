from pydantic import BaseModel
from uuid import UUID


class PageCreate(BaseModel):
    image_url: str
    page_number: int


class PageOut(BaseModel):
    id: UUID
    chapter_id: UUID
    image_url: str
    page_number: int

    class Config:
        from_attributes = True