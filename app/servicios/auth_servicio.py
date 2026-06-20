# app/services/auth_service.py

from sqlalchemy.orm import Session

from app.modelos.usuarios import User
from app.esquemas.usuarios import UserCreate, UserLogin
from app.core.security_breach import hash_password, verify_password
from app.core.auth import create_access_token


def create_user(db: Session, user_data: UserCreate):
    existing_user = db.query(User).filter(
        (User.email == user_data.email) |
        (User.username == user_data.username)
    ).first()

    if existing_user:
        return None

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(db: Session, login_data: UserLogin):
    user = db.query(User).filter(
        User.email == login_data.email
    ).first()

    if not user:
        return None

    if not verify_password(login_data.password, user.password_hash):
        return None

    token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }