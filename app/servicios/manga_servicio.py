from sqlalchemy.orm import Session
from uuid import UUID

from app.modelos.manga import Manga
from app.esquemas.manga import (
    MangaCreate,
    MangaUpdate
)


def create_manga(
    db: Session,
    user_id: UUID,
    manga_data: MangaCreate
):
    new_manga = Manga(
        author_id=user_id,
        title=manga_data.title,
        description=manga_data.description,
        cover_url=manga_data.cover_url
    )

    db.add(new_manga)
    db.commit()
    db.refresh(new_manga)

    return new_manga


def get_all_mangas(db: Session):
    return db.query(Manga).all()


def get_manga_by_id(
    db: Session,
    manga_id: UUID
):
    return db.query(Manga).filter(
        Manga.id == manga_id
    ).first()


def get_user_mangas(
    db: Session,
    user_id: UUID
):
    return db.query(Manga).filter(
        Manga.author_id == user_id
    ).all()


def update_manga(
    db: Session,
    manga_id: UUID,
    manga_data: MangaUpdate
):
    manga = db.query(Manga).filter(
        Manga.id == manga_id
    ).first()

    if not manga:
        return None

    update_data = manga_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(manga, key, value)

    db.commit()
    db.refresh(manga)

    return manga


def delete_manga(
    db: Session,
    manga_id: UUID
):
    manga = db.query(Manga).filter(
        Manga.id == manga_id
    ).first()

    if not manga:
        return False

    db.delete(manga)
    db.commit()

    return True