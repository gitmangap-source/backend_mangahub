from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modelos.manga import Manga


def validate_manga_owner(
    db: Session,
    manga_id: UUID,
    user_id: UUID
):
    manga = (
        db.query(Manga)
        .filter(Manga.id == manga_id)
        .first()
    )

    if not manga:
        raise HTTPException(
            status_code=404,
            detail="Manga no encontrado"
        )

    if manga.author_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="No autorizado"
        )

    return manga