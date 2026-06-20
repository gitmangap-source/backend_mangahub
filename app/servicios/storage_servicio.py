import uuid
import os
import httpx
from fastapi import HTTPException, UploadFile, status
from app.core.config import settings

# ----------------------------------------------------
# 1. INICIALIZACIÓN DE CLIENTES (según el tipo)
# ----------------------------------------------------

supabase_client = None
if settings.STORAGE_TYPE == "supabase":
    from supabase import create_client, Client
    supabase_client: Client = create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_SERVICE_KEY
    )

# ----------------------------------------------------
# 2. FUNCIÓN PRINCIPAL DE SUBIDA (UNA SOLA LECTURA)
# ----------------------------------------------------

async def upload_file(file: UploadFile, folder: str) -> str:
    """
    Sube un archivo a la carpeta especificada ('covers' o 'pages')
    y devuelve la URL pública para guardar en la BD.
    """
    # Validaciones comunes (tamaño y tipo)
    ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
    MAX_SIZE = 20 * 1024 * 1024  # 20 MB

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Formato no permitido. Solo JPG, PNG o WEBP."
        )

    # 🔹 LECTURA ÚNICA DEL ARCHIVO (ocurre solo aquí)
    contents = await file.read()

    if len(contents) > MAX_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Archivo demasiado grande (máx 20 MB)"
        )

    # Generar nombre único
    extension = file.filename.split(".")[-1] if file.filename else "jpg"
    if extension.lower() not in ["jpg", "jpeg", "png", "webp"]:
        extension = "jpg"
    file_name = f"{uuid.uuid4()}.{extension}"
    storage_path = f"{folder}/{file_name}"

    # ----------------------------------------------------
    # REDIRIGIR SEGÚN EL TIPO DE ALMACENAMIENTO
    # (se pasa el contenido ya leído, no el objeto file)
    # ----------------------------------------------------
    if settings.STORAGE_TYPE == "local":
        return await _upload_local(storage_path, contents, file.content_type)

    elif settings.STORAGE_TYPE == "supabase":
        return await _upload_supabase(storage_path, contents, file.content_type)

    elif settings.STORAGE_TYPE == "external":
        return await _upload_external(storage_path, contents, file.content_type)

    else:
        raise HTTPException(
            status_code=500,
            detail="STORAGE_TYPE no válido en la configuración."
        )

# ----------------------------------------------------
# 3. IMPLEMENTACIONES ESPECÍFICAS (reciben bytes directamente)
# ----------------------------------------------------

async def _upload_local(storage_path: str, contents: bytes, content_type: str) -> str:
    """Guarda el archivo en el sistema de archivos local y devuelve la URL pública."""
    base_dir = settings.LOCAL_STORAGE_PATH
    full_path = os.path.join(base_dir, storage_path)

    # Crear directorios si no existen
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    # Guardar archivo directamente con los bytes recibidos (sin volver a leer)
    with open(full_path, "wb") as f:
        f.write(contents)

    # Construir URL pública (asumiendo que FastAPI sirve /static)
    return f"{settings.PUBLIC_BASE_URL}/static/{storage_path}"


async def _upload_supabase(storage_path: str, contents: bytes, content_type: str) -> str:
    """Sube el archivo a Supabase Storage y devuelve la URL pública."""
    global supabase_client
    if supabase_client is None:
        raise HTTPException(
            status_code=500,
            detail="Cliente de Supabase no inicializado."
        )

    # Subir al bucket (contents ya son bytes, sin necesidad de leer de nuevo)
    try:
        supabase_client.storage.from_(settings.SUPABASE_BUCKET).upload(
            path=storage_path,
            file=contents,
            file_options={"content-type": content_type}
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al subir a Supabase: {str(e)}"
        )

    # Obtener URL pública
    public_url = supabase_client.storage.from_(settings.SUPABASE_BUCKET).get_public_url(storage_path)
    return public_url


async def _upload_external(storage_path: str, contents: bytes, content_type: str) -> str:
    """Envía el archivo a una PC externa mediante una API HTTP."""
    if not settings.EXTERNAL_STORAGE_URL:
        raise HTTPException(
            status_code=500,
            detail="EXTERNAL_STORAGE_URL no configurada."
        )

    # Preparar multipart form data con los bytes ya leídos
    files = {
        "file": (storage_path, contents, content_type)
    }
    headers = {
        "X-API-Key": settings.EXTERNAL_API_KEY or ""
    }

    async with httpx.AsyncClient() as client:
        try:
            # Se asume que la PC externa tiene un endpoint /upload
            response = await client.post(
                f"{settings.EXTERNAL_STORAGE_URL}/upload",
                files=files,
                headers=headers,
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            return data["url"]
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al subir a PC externa: {str(e)}"
            )