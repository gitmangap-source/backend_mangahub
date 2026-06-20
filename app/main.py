import os
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine
from app.core.config import settings
from app.modelos import usuarios, manga, capitulo, pagina  # importa TODOS los modelos

from app.rutas.auth import router as auth_router
from app.rutas.manga import router as manga_router
from app.rutas.capitulo import router as chapter_router
from app.rutas.lector import router as reader_router
from app.rutas.upload import router as upload_router


app = FastAPI(
    title="MangaHub API",
    version="1.0.0",
    description="API para publicación y lectura de mangas y manwhas"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5500",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Rutas
app.include_router(
    auth_router,
    prefix="/api/auth",
    tags=["Auth"]
)

app.include_router(
    manga_router,
    prefix="/api/mangas",
    tags=["Mangas"]
)

app.include_router(
    chapter_router,
    prefix="/api/chapters",
    tags=["Chapters"]
)

app.include_router(
    reader_router,
    prefix="/api/reader",
    tags=["Reader"]
)

app.include_router(
    upload_router,
    prefix="/api/upload",
    tags=["Upload"]
)


@app.get("/")
def root():
    return {
        "message": "MangaHub API Online"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }
    
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    if settings.STORAGE_TYPE == "local":
        os.makedirs(settings.LOCAL_STORAGE_PATH, exist_ok=True)
        app.mount("/static", StaticFiles(directory=settings.LOCAL_STORAGE_PATH), name="static")



print("TABLAS:", Base.metadata.tables.keys())