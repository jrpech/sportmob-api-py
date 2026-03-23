"""
Router para servir archivos multimedia con autenticación
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from pathlib import Path
import os

from app.config import settings
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/media", tags=["Media"])


@router.get("/{path:path}")
async def obtener_archivo(
    path: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene un archivo multimedia protegido por autenticación.
    
    Solo usuarios autenticados pueden acceder a los archivos.
    
    **Path Params:**
    - `path`: Ruta relativa del archivo (ej: historias/2024/03/23/archivo.jpg)
    
    **Requiere**: Token JWT válido
    """
    # Construir ruta completa del archivo
    archivo_path = Path(settings.UPLOAD_DIR) / path
    
    # Validaciones de seguridad
    # 1. Verificar que el archivo existe
    if not archivo_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Archivo no encontrado"
        )
    
    # 2. Verificar que es un archivo (no directorio)
    if not archivo_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ruta inválida"
        )
    
    # 3. Verificar que el archivo está dentro del directorio de uploads
    # (prevenir path traversal attacks)
    upload_dir_abs = Path(settings.UPLOAD_DIR).resolve()
    archivo_abs = archivo_path.resolve()
    
    if not str(archivo_abs).startswith(str(upload_dir_abs)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado"
        )
    
    # Determinar tipo de contenido basado en extensión
    extension = archivo_path.suffix.lower()
    
    media_types = {
        # Imágenes
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
        # Videos
        '.mp4': 'video/mp4',
        '.mov': 'video/quicktime',
        '.avi': 'video/x-msvideo',
        '.webm': 'video/webm',
    }
    
    media_type = media_types.get(extension, 'application/octet-stream')
    
    # Retornar archivo
    return FileResponse(
        path=str(archivo_abs),
        media_type=media_type,
        filename=archivo_path.name
    )


@router.get("/public/{path:path}")
async def obtener_archivo_publico(path: str):
    """
    Obtiene archivos públicos sin autenticación (ej: fotos de perfil).
    
    Solo permite acceso a carpetas específicas marcadas como públicas.
    """
    # Lista de carpetas permitidas para acceso público
    carpetas_publicas = ["perfiles", "logos", "banners"]
    
    # Verificar que la ruta comienza con una carpeta pública
    primera_carpeta = path.split('/')[0] if '/' in path else path
    
    if primera_carpeta not in carpetas_publicas:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso no permitido a esta carpeta"
        )
    
    # Construir ruta completa del archivo
    archivo_path = Path(settings.UPLOAD_DIR) / path
    
    # Validaciones de seguridad (mismo que el endpoint protegido)
    if not archivo_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Archivo no encontrado"
        )
    
    if not archivo_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ruta inválida"
        )
    
    upload_dir_abs = Path(settings.UPLOAD_DIR).resolve()
    archivo_abs = archivo_path.resolve()
    
    if not str(archivo_abs).startswith(str(upload_dir_abs)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado"
        )
    
    # Determinar tipo de contenido
    extension = archivo_path.suffix.lower()
    media_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
    }
    
    media_type = media_types.get(extension, 'application/octet-stream')
    
    return FileResponse(
        path=str(archivo_abs),
        media_type=media_type,
        filename=archivo_path.name
    )
