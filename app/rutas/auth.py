# app/routes/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.esquemas.auth import Token
from app.db.database import get_db
from app.esquemas.usuarios import UserCreate, UserLogin, UserOut
from app.servicios.auth_servicio import create_user, login_user
from app.dependencias.auth import get_current_user
from app.modelos.usuarios import User
from app.dependencias.auth import get_current_user

router = APIRouter()


# aquui esta el endpoint para regsitrar 

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):

    new_user = create_user(db, user)

    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario o email ya existe"
        )

    return new_user

#aqui va el login: -> https://www.google.com/search?sca_esv=4063fbd0dbfac657&sxsrf=ANbL-n58m1KmLTT12lV-ffPTY6ka133qRg:1780779832824&udm=2&fbs=ADc_l-bpk8W4E-qsVlOvbGJcDwpn60DczFdcvPnuv8WQohHLTaf9fS4tJ71bi2aHS-Pmeg3gf3Rx3g7wPLd9qB5u5EuZYeuURw-LEmpdoZ-f8DEVyumGGLE--MFWuCP3KDx6YC9r1-ipkAmWZwMeKBvepgLTa4kAJEnrnBtFOiDDclJxtAE3grY3Pm2gQrBEOHOvrYkPaqY30P-wz444_xLOo5EwT_W81w&q=ponido+aqui+meme&sa=X&ved=2ahUKEwiBgO_qwfOUAxUVSjABHc52DUcQtKgLegQIExAB&biw=697&bih=632&dpr=1.38#sv=CAMSVhoyKhBlLTNGcUxTT1gtTjdxRVZNMg4zRnFMU09YLU43cUVWTToORFlRSDdnSXVXcjlULU0gBCocCgZtb3NhaWMSEGUtM0ZxTFNPWC1ON3FFVk0YADABGAcg2fLbvAtKCBABGAEgASgB

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):

    token_data = login_user(db, user)

    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    return token_data

# wea para ver el perfil del usuario 

@router.get(
    "/me",
    response_model=UserOut
)
def me(
    current_user: User = Depends(get_current_user)
):
    return current_user