from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # API
    APP_NAME: str = "MangaHub API"
    APP_VERSION: str = "1.0.0"

    # Database
    DATABASE_URL: str

    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080

    # --- NUEVA CONFIGURACIÓN DE ALMACENAMIENTO ---
    # Opciones: "local", "supabase", "external"
    STORAGE_TYPE: str = "local"

    # URL base para construir los enlaces públicos (ej: http://localhost:8000 o https://tudominio.com)
    PUBLIC_BASE_URL: str = "http://localhost:8000"

    # 1) Configuración para Supabase
    SUPABASE_URL: str | None = None
    SUPABASE_SERVICE_KEY: str | None = None  # Usa service_role para subir desde el backend
    SUPABASE_BUCKET: str = "mangahub"        # El nombre del bucket en Supabase

    # 2) Configuración para almacenamiento local (PC interna o externa montada)
    LOCAL_STORAGE_PATH: str = "static"       # Carpeta donde se guardarán los archivos

    # 3) Configuración para PC externa (si tiene una API propia)
    EXTERNAL_STORAGE_URL: str | None = None  # Ej: "https://storage.mipc.com/upload"
    EXTERNAL_API_KEY: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()