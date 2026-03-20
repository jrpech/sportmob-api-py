from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.config import settings
from app.routers import login, historia

# Crear instancia de FastAPI
app = FastAPI(
    title="API SportMob Python",
    description="API en Python compatible con JWT de la API .NET existente",
    version="1.0.0",
    docs_url="/swagger",
    redoc_url="/redoc"
)

# Configurar CORS (igual que en .NET)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear directorio de uploads si no existe
upload_dir = Path(settings.UPLOAD_DIR)
upload_dir.mkdir(parents=True, exist_ok=True)

# Montar directorio de uploads como archivos estáticos
app.mount("/uploads", StaticFiles(directory=str(upload_dir)), name="uploads")

# Incluir routers
app.include_router(login.router)
app.include_router(historia.router)


@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "API SportMob Python",
        "version": "1.0.0",
        "status": "running",
        "docs": "/swagger",
        "features": ["JWT Auth", "Historias/Stories"]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
