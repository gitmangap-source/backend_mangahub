from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.esquemas.capitulo import ChapterCreate, ChapterOut
from app.esquemas.pagina import PageCreate, PageOut

from app.servicios.capitulo_servicio import (
    create_chapter,
    add_pages_to_chapter
)

from app.dependencias.auth import get_current_user
from app.dependencias.manga import validate_manga_owner

from app.modelos.usuarios import User
from app.modelos.manga import Manga
from app.modelos.capitulo import Chapter

router = APIRouter()


@router.post("/manga/{manga_id}", response_model=ChapterOut)
def create_new_chapter(
    manga_id: UUID,
    chapter: ChapterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    validate_manga_owner(
        db,
        manga_id,
        current_user.id
    )

    return create_chapter(
        db=db,
        manga_id=manga_id,
        chapter_data=chapter
    )


@router.post("/{chapter_id}/pages", response_model=list[PageOut])
def upload_pages(
    chapter_id: UUID,
    pages: list[PageCreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chapter = db.query(Chapter).filter(
        Chapter.id == chapter_id
    ).first()

    if not chapter:
        raise HTTPException(
            status_code=404,
            detail="Capítulo no encontrado"
        )

    manga = db.query(Manga).filter(
        Manga.id == chapter.manga_id
    ).first()

    if manga.author_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="No puedes modificar este capítulo"
        )

    return add_pages_to_chapter(
        db=db,
        chapter_id=chapter_id,
        pages=pages
    )


@router.get("/{chapter_id}", response_model=ChapterOut)
def get_chapter(
    chapter_id: UUID,
    db: Session = Depends(get_db)
):
    chapter = db.query(Chapter).filter(
        Chapter.id == chapter_id
    ).first()

    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Capítulo no encontrado"
        )

    return chapter