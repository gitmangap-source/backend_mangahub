# app/services/reader_service.py

from sqlalchemy.orm import Session
from uuid import UUID
from app.modelos.capitulo import Chapter
from app.modelos.pagina import Page
from app.esquemas.capitulo import ChapterOut
from app.esquemas.pagina import PageOut

# ordena las paginas 
def get_chapter_with_pages(db: Session, chapter_id: UUID):
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()

    if not chapter:
        return None

    pages = (
        db.query(Page)
        .filter(Page.chapter_id == chapter_id)
        .order_by(Page.page_number.asc())
        .all()
    )

    return {
        "chapter": ChapterOut.model_validate(chapter),
        "pages": [PageOut.model_validate(page) for page in pages]
    }