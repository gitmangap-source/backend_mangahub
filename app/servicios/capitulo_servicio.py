from sqlalchemy.orm import Session
from uuid import UUID

from app.modelos.capitulo import Chapter
from app.modelos.pagina import Page
from app.esquemas.capitulo import ChapterCreate
from app.esquemas.pagina import PageCreate


def create_chapter(db: Session, manga_id: UUID, chapter_data: ChapterCreate):

    new_chapter = Chapter(
        manga_id=manga_id,
        title=chapter_data.title,
        chapter_number=chapter_data.chapter_number
    )

    db.add(new_chapter)
    db.commit()
    db.refresh(new_chapter)

    return new_chapter


def add_pages_to_chapter(
    db: Session,
    chapter_id: UUID,
    pages: list[PageCreate]
):

    page_objects = []

    for page in pages:

        new_page = Page(
            chapter_id=chapter_id,
            image_url=page.image_url,
            page_number=page.page_number
        )

        page_objects.append(new_page)

    db.add_all(page_objects)
    db.commit()
    
    for page in page_objects:
        db.refresh(page)

    return page_objects