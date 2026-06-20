# app/routes/reader.py

from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.servicios.lector_servicio import get_chapter_with_pages
from app.esquemas.lector import ChapterWithPagesOut

router = APIRouter()


@router.get("/read/{chapter_id}", response_model=ChapterWithPagesOut)
def read_chapter(chapter_id: UUID, db: Session = Depends(get_db)):

    result = get_chapter_with_pages(db, chapter_id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Capítulo no encontrado"
        )

    return result