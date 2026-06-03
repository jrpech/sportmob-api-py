"""
Utilidades para procesamiento de imágenes y videos
"""
import base64
import binascii
from PIL import Image
from typing import Tuple, Optional
import os
from pathlib import Path
from datetime import datetime
from app.config import settings


def crear_miniatura(ruta_imagen: str, ruta_salida: str, tamano: Tuple[int, int] = None) -> str:
    """
    Crea una miniatura de una imagen
    
    Args:
        ruta_imagen: Ruta de la imagen original
        ruta_salida: Ruta donde guardar la miniatura
        tamano: Tupla con (ancho, alto). Si es None, usa configuración default
    
    Returns:
        Ruta de la miniatura generada
    """
    if tamano is None:
        tamano = settings.HISTORIA_MINIATURA_SIZE
    
    try:
        with Image.open(ruta_imagen) as img:
            # Convertir a RGB si es necesario (para manejar PNG con transparencia)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Crear fondo blanco
                fondo = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                fondo.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = fondo
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Crear miniatura manteniendo aspect ratio
            img.thumbnail(tamano, Image.Resampling.LANCZOS)
            
            # Guardar miniatura
            img.save(ruta_salida, 'JPEG', quality=85, optimize=True)
            
        return ruta_salida
    except Exception as e:
        raise Exception(f"Error creando miniatura: {str(e)}")


def obtener_dimensiones_imagen(ruta_imagen: str) -> Tuple[int, int]:
    """
    Obtiene las dimensiones de una imagen
    
    Returns:
        Tupla con (ancho, alto)
    """
    try:
        with Image.open(ruta_imagen) as img:
            return img.size
    except Exception as e:
        raise Exception(f"Error obteniendo dimensiones: {str(e)}")


def es_formato_imagen_valido(extension: str) -> bool:
    """
    Verifica si la extensión es de un formato de imagen válido
    """
    return extension.lower() in settings.ALLOWED_IMAGE_EXTENSIONS


def es_formato_video_valido(extension: str) -> bool:
    """
    Verifica si la extensión es de un formato de video válido
    """
    return extension.lower() in settings.ALLOWED_VIDEO_EXTENSIONS


def obtener_extension_archivo(nombre_archivo: str) -> str:
    """
    Obtiene la extensión de un archivo (incluyendo el punto)
    """
    _, ext = os.path.splitext(nombre_archivo)
    return ext.lower()


def validar_tamano_archivo(tamano_bytes: int) -> bool:
    """
    Valida que el tamaño del archivo esté dentro del límite
    """
    max_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    return tamano_bytes <= max_bytes


def sanitizar_nombre_archivo(nombre: str) -> str:
    """
    Sanitiza el nombre del archivo eliminando caracteres peligrosos
    """
    # Eliminar caracteres peligrosos
    caracteres_invalidos = ['/', '\\', '..', '<', '>', ':', '"', '|', '?', '*']
    nombre_limpio = nombre
    
    for char in caracteres_invalidos:
        nombre_limpio = nombre_limpio.replace(char, '_')
    
    return nombre_limpio


def save_image_base64(base64img: str, id_value: int, texto: str, tipo: str) -> str:
    """
    Guarda una imagen en base64 en Resources/<tipo> y devuelve el nombre del archivo.
    Si ocurre un error, devuelve un string con prefijo "Error:" para compatibilidad.
    """
    try:
        folder_path = Path.cwd() / "Resources" / tipo
        folder_path.mkdir(parents=True, exist_ok=True)

        # Soporta formatos como: data:image/png;base64,AAAA...
        base64_clean = base64img.split(",", 1)[1] if "," in base64img else base64img
        image_bytes = base64.b64decode(base64_clean, validate=True)

        now = datetime.now()
        time_part = f"{now.hour}-{now.minute}-{now.second}-{int(now.microsecond / 1000)}"
        image_name = f"{texto}{id_value}{time_part}.png"

        file_path = folder_path / image_name
        with open(file_path, "wb") as image_file:
            image_file.write(image_bytes)

        return image_name
    except (binascii.Error, ValueError) as ex:
        return f"Error: base64 inválido ({str(ex)})"
    except Exception as ex:
        return f"Error: {str(ex)}"
