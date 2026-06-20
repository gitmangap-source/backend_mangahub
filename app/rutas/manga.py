from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.modelos.usuarios import User

from app.dependencias.auth import get_current_user
from app.dependencias.manga import validate_manga_owner

from app.esquemas.manga import (
    MangaCreate,
    MangaUpdate,
    MangaOut
)

from app.servicios.manga_servicio import (
    create_manga,
    get_all_mangas,
    get_manga_by_id,
    get_user_mangas,
    update_manga,
    delete_manga
)

router = APIRouter()


@router.post(
    "/",
    response_model=MangaOut
)
def create_new_manga(
    manga: MangaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_manga(
        db=db,
        user_id=current_user.id,
        manga_data=manga
    )


@router.get(
    "/",
    response_model=list[MangaOut]
)
def list_mangas(
    db: Session = Depends(get_db)
):
    return get_all_mangas(db)


@router.get(
    "/mine",
    response_model=list[MangaOut]
)
def my_mangas(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_user_mangas(
        db,
        current_user.id
    )


@router.get(
    "/{manga_id}",
    response_model=MangaOut
)
def get_manga(
    manga_id: UUID,
    db: Session = Depends(get_db)
):
    manga = get_manga_by_id(
        db,
        manga_id
    )

    if not manga:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manga no encontrado"
        )

    return manga


@router.put(
    "/{manga_id}",
    response_model=MangaOut
)
def edit_manga(
    manga_id: UUID,
    manga_data: MangaUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    validate_manga_owner(
        db,
        manga_id,
        current_user.id
    )

    return update_manga(
        db,
        manga_id,
        manga_data
    )


@router.delete(
    "/{manga_id}"
)
def remove_manga(
    manga_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    validate_manga_owner(
        db,
        manga_id,
        current_user.id
    )

    delete_manga(
        db,
        manga_id
    )

    return {
        "message": "Manga eliminado"
    }