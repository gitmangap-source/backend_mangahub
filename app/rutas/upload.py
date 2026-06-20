from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends
from app.dependencias.auth import get_current_user 
from app.servicios.storage_servicio import upload_file
from app.modelos.usuarios import User

router = APIRouter()

@router.post("/cover")
async def upload_cover(  # ← async
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    url = await upload_file(file, "covers")  # ← await
    return {"url": url}

@router.post("/pages")
async def upload_page(   # ← async
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    url = await upload_file(file, "pages")   # ← await
    return {"url": url}
