from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    # JWT Configuration - DEBE SER IDENTICA A LA DE .NET
    JWT_SECRET_KEY: str = "VaibhavBhapkarVaibhavBhapkar"
    JWT_ISSUER: str = "https://localhost:5001/"
    JWT_AUDIENCE: str = "https://localhost:5001/"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 43200  # 30 días
    
    # Database Configuration
    DB_HOST: str = "db"
    DB_PORT: int = 3306
    DB_NAME: str = "pruebasliguilla"
    DB_USER: str = "root"
    DB_PASSWORD: str = "rootroot"
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    
    # CORS Origins
    CORS_ORIGINS: str = "http://localhost:51297,http://tamara.digimob.mx"
    
    # Almacenamiento de Archivos
    STORAGE_TYPE: str = "local"  # "local" o "s3"
    UPLOAD_DIR: str = "/app/uploads"
    BASE_URL: str = "http://localhost:8000"  # URL base para acceder a archivos
    MAX_FILE_SIZE_MB: int = 50  # 50 MB
    
    # Historias
    HISTORIA_EXPIRACION_HORAS: int = 24
    HISTORIA_VIDEO_MAX_SEGUNDOS: int = 30
    HISTORIA_MINIATURA_SIZE: tuple = (300, 300)
    
    # S3 Configuration (para futuro)
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_S3_BUCKET: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    CDN_URL: Optional[str] = None
    
    # Extensiones permitidas
    ALLOWED_IMAGE_EXTENSIONS: set = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    ALLOWED_VIDEO_EXTENSIONS: set = {".mp4", ".mov", ".avi", ".webm"}
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    @property
    def database_url(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def allowed_extensions(self) -> set:
        return self.ALLOWED_IMAGE_EXTENSIONS | self.ALLOWED_VIDEO_EXTENSIONS
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
