"""
Servicio de almacenamiento de archivos
Soporta almacenamiento local y S3 (preparado para migración)
"""
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple
import uuid
from fastapi import UploadFile

from app.config import settings
from app.utils.image_utils import (
    sanitizar_nombre_archivo,
    obtener_extension_archivo,
    validar_tamano_archivo
)


class StorageService:
    """
    Servicio de almacenamiento abstracto
    Actualmente usa almacenamiento local, preparado para migrar a S3
    """
    
    def __init__(self):
        self.storage_type = settings.STORAGE_TYPE
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Crea los directorios necesarios si no existen"""
        directories = [
            self.upload_dir / "historias",
            self.upload_dir / "historias" / "miniaturas",
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _generar_nombre_unico(self, extension: str, prefijo: str = "historia") -> str:
        """
        Genera un nombre único para el archivo
        
        Format: prefijo_timestamp_uuid.ext
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        return f"{prefijo}_{timestamp}_{unique_id}{extension}"
    
    def _obtener_ruta_fecha(self) -> Path:
        """
        Obtiene el path organizado por fecha: YYYY/MM/DD
        """
        ahora = datetime.now()
        return Path(str(ahora.year)) / f"{ahora.month:02d}" / f"{ahora.day:02d}"
    
    async def guardar_archivo(
        self, 
        archivo: UploadFile,
        tipo: str = "historia",
        usuario_id: Optional[int] = None
    ) -> Tuple[str, str, int]:
        """
        Guarda un archivo en el sistema de almacenamiento
        
        Args:
            archivo: Archivo a guardar
            tipo: Tipo de archivo (historia, perfil, etc.)
            usuario_id: ID del usuario (opcional, para organización)
        
        Returns:
            Tupla con (ruta_relativa, ruta_completa, tamano_bytes)
        
        Raises:
            Exception: Si hay error al guardar
        """
        # Validar extensión
        extension = obtener_extension_archivo(archivo.filename)
        if extension not in settings.allowed_extensions:
            raise ValueError(f"Extensión no permitida: {extension}")
        
        # Leer contenido del archivo
        contenido = await archivo.read()
        tamano_bytes = len(contenido)
        
        # Validar tamaño
        if not validar_tamano_archivo(tamano_bytes):
            raise ValueError(
                f"Archivo demasiado grande. Máximo: {settings.MAX_FILE_SIZE_MB}MB"
            )
        
        # Generar nombre único
        nombre_archivo = self._generar_nombre_unico(extension, tipo)
        
        # Construir path: upload_dir/historias/YYYY/MM/DD/archivo.ext
        ruta_fecha = self._obtener_ruta_fecha()
        directorio_completo = self.upload_dir / "historias" / ruta_fecha
        directorio_completo.mkdir(parents=True, exist_ok=True)
        
        # Ruta completa del archivo
        ruta_completa = directorio_completo / nombre_archivo
        
        # Guardar archivo
        try:
            with open(ruta_completa, "wb") as f:
                f.write(contenido)
        except Exception as e:
            raise Exception(f"Error guardando archivo: {str(e)}")
        
        # Retornar ruta relativa (para URL)
        ruta_relativa = f"historias/{ruta_fecha}/{nombre_archivo}"
        
        return ruta_relativa, str(ruta_completa), tamano_bytes
    
    async def guardar_miniatura(
        self,
        ruta_original: str,
        nombre_base: str
    ) -> str:
        """
        Guarda una miniatura
        
        Args:
            ruta_original: Ruta del archivo original
            nombre_base: Nombre base para la miniatura
        
        Returns:
            Ruta relativa de la miniatura
        """
        # Construir path para miniatura
        ruta_fecha = self._obtener_ruta_fecha()
        directorio_miniaturas = self.upload_dir / "historias" / "miniaturas" / ruta_fecha
        directorio_miniaturas.mkdir(parents=True, exist_ok=True)
        
        nombre_miniatura = f"thumb_{nombre_base}.jpg"
        ruta_miniatura = directorio_miniaturas / nombre_miniatura
        
        # La miniatura se crea en otro servicio (image_utils)
        # Aquí solo retornamos la ruta donde debería estar
        
        ruta_relativa = f"historias/miniaturas/{ruta_fecha}/{nombre_miniatura}"
        return ruta_relativa
    
    def eliminar_archivo(self, ruta_relativa: str) -> bool:
        """
        Elimina un archivo del almacenamiento
        
        Args:
            ruta_relativa: Ruta relativa del archivo
        
        Returns:
            True si se eliminó correctamente
        """
        ruta_completa = self.upload_dir / ruta_relativa
        
        try:
            if ruta_completa.exists():
                ruta_completa.unlink()
                return True
        except Exception as e:
            print(f"Error eliminando archivo: {str(e)}")
        
        return False
    
    def obtener_url_publica(self, ruta_relativa: str) -> str:
        """
        Obtiene la URL pública del archivo
        
        Args:
            ruta_relativa: Ruta relativa del archivo
        
        Returns:
            URL completa del archivo
        """
        if self.storage_type == "s3" and settings.CDN_URL:
            # Futuro: retornar URL de CDN
            return f"{settings.CDN_URL}/{ruta_relativa}"
        else:
            # Local: retornar URL del servidor
            return f"{settings.BASE_URL}/uploads/{ruta_relativa}"
    
    def obtener_ruta_completa(self, ruta_relativa: str) -> str:
        """
        Obtiene la ruta completa del archivo en el sistema local
        
        Args:
            ruta_relativa: Ruta relativa del archivo
        
        Returns:
            Ruta completa en el sistema de archivos
        """
        return str(self.upload_dir / ruta_relativa)


# Instancia global del servicio
storage_service = StorageService()
