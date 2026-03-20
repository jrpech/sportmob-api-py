"""
Servicio de lógica de negocio para Historias
"""
from datetime import datetime, timedelta
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from fastapi import UploadFile

from app.models import Historia, HistoriaVista, HistoriaReaccion, Usuario, TipoHistoria
from app.schemas import HistoriaCreate
from app.config import settings
from app.services.storage_service import storage_service
from app.utils.image_utils import (
    crear_miniatura,
    obtener_dimensiones_imagen,
    es_formato_imagen_valido,
    es_formato_video_valido,
    obtener_extension_archivo
)


class HistoriaService:
    """
    Servicio para gestionar historias
    """
    
    @staticmethod
    def calcular_fecha_expiracion(destacada: bool = False) -> Optional[datetime]:
        """
        Calcula la fecha de expiración de una historia
        
        Args:
            destacada: Si es destacada, no expira
        
        Returns:
            Fecha de expiración o None si es destacada
        """
        if destacada:
            return None
        
        return datetime.utcnow() + timedelta(hours=settings.HISTORIA_EXPIRACION_HORAS)
    
    @staticmethod
    async def crear_historia(
        db: Session,
        usuario_id: int,
        archivo: UploadFile,
        data: HistoriaCreate
    ) -> Historia:
        """
        Crea una nueva historia
        
        Args:
            db: Sesión de base de datos
            usuario_id: ID del usuario que crea la historia
            archivo: Archivo de imagen o video
            data: Datos adicionales de la historia
        
        Returns:
            Historia creada
        
        Raises:
            ValueError: Si hay error de validación
            Exception: Si hay error al procesar
        """
        # Validar extensión y determinar tipo
        extension = obtener_extension_archivo(archivo.filename)
        
        if es_formato_imagen_valido(extension):
            tipo = TipoHistoria.imagen
        elif es_formato_video_valido(extension):
            tipo = TipoHistoria.video
        else:
            raise ValueError(f"Formato de archivo no soportado: {extension}")
        
        # Guardar archivo
        ruta_relativa, ruta_completa, tamano_bytes = await storage_service.guardar_archivo(
            archivo=archivo,
            tipo="historia",
            usuario_id=usuario_id
        )
        
        # Obtener URL pública
        url_archivo = storage_service.obtener_url_publica(ruta_relativa)
        
        # Crear miniatura solo para imágenes
        url_miniatura = None
        ancho = None
        alto = None
        duracion_video = None
        
        if tipo == TipoHistoria.imagen:
            try:
                # Obtener dimensiones
                ancho, alto = obtener_dimensiones_imagen(ruta_completa)
                
                # Crear miniatura
                nombre_base = ruta_relativa.split('/')[-1].replace(extension, '')
                ruta_miniatura_relativa = await storage_service.guardar_miniatura(
                    ruta_original=ruta_completa,
                    nombre_base=nombre_base
                )
                
                # Generar miniatura física
                ruta_miniatura_completa = storage_service.obtener_ruta_completa(
                    ruta_miniatura_relativa
                )
                crear_miniatura(ruta_completa, ruta_miniatura_completa)
                
                url_miniatura = storage_service.obtener_url_publica(ruta_miniatura_relativa)
                
            except Exception as e:
                print(f"Error creando miniatura: {str(e)}")
                # Continuar sin miniatura
        
        elif tipo == TipoHistoria.video:
            # TODO: Para videos, extraer frame para miniatura y obtener duración
            # Por ahora, usar valores por defecto
            ancho = 1080
            alto = 1920
            duracion_video = settings.HISTORIA_VIDEO_MAX_SEGUNDOS
        
        # Calcular fecha de expiración
        fecha_expiracion = HistoriaService.calcular_fecha_expiracion(data.destacada)
        
        # Crear registro en BD
        historia = Historia(
            usuario_id=usuario_id,
            tipo=tipo,
            url_archivo=url_archivo,
            url_miniatura=url_miniatura,
            nombre_archivo=archivo.filename,
            descripcion=data.descripcion,
            duracion_segundos=data.duracion_segundos,
            ancho=ancho,
            alto=alto,
            tamano_bytes=tamano_bytes,
            duracion_video=duracion_video,
            fecha_expiracion=fecha_expiracion,
            destacada=data.destacada,
            activa=True,
            vistas_totales=0
        )
        
        db.add(historia)
        db.commit()
        db.refresh(historia)
        
        return historia
    
    @staticmethod
    def obtener_historias_activas(
        db: Session,
        incluir_expiradas: bool = False
    ) -> List[Historia]:
        """
        Obtiene todas las historias activas
        
        Args:
            db: Sesión de base de datos
            incluir_expiradas: Si incluir historias expiradas
        
        Returns:
            Lista de historias
        """
        query = db.query(Historia).filter(Historia.activa == True)
        
        if not incluir_expiradas:
            ahora = datetime.utcnow()
            query = query.filter(
                or_(
                    Historia.fecha_expiracion.is_(None),  # Destacadas
                    Historia.fecha_expiracion > ahora  # No expiradas
                )
            )
        
        return query.order_by(Historia.fecha_creacion.desc()).all()
    
    @staticmethod
    def obtener_historias_usuario(
        db: Session,
        usuario_id: int,
        solo_activas: bool = True
    ) -> List[Historia]:
        """
        Obtiene las historias de un usuario específico
        """
        query = db.query(Historia).filter(Historia.usuario_id == usuario_id)
        
        if solo_activas:
            query = query.filter(Historia.activa == True)
            ahora = datetime.utcnow()
            query = query.filter(
                or_(
                    Historia.fecha_expiracion.is_(None),
                    Historia.fecha_expiracion > ahora
                )
            )
        
        return query.order_by(Historia.fecha_creacion.desc()).all()
    
    @staticmethod
    def marcar_como_vista(
        db: Session,
        historia_id: int,
        usuario_id: int,
        tiempo_visto: int = 0,
        completo: bool = True
    ) -> HistoriaVista:
        """
        Marca una historia como vista
        
        Returns:
            HistoriaVista creada o existente
        """
        # Verificar si ya existe la vista
        vista_existente = db.query(HistoriaVista).filter(
            and_(
                HistoriaVista.historia_id == historia_id,
                HistoriaVista.usuario_id == usuario_id
            )
        ).first()
        
        if vista_existente:
            # Actualizar si es necesario
            vista_existente.tiempo_visto_segundos = max(
                vista_existente.tiempo_visto_segundos,
                tiempo_visto
            )
            vista_existente.completo = vista_existente.completo or completo
            db.commit()
            db.refresh(vista_existente)
            return vista_existente
        
        # Crear nueva vista
        vista = HistoriaVista(
            historia_id=historia_id,
            usuario_id=usuario_id,
            tiempo_visto_segundos=tiempo_visto,
            completo=completo
        )
        
        db.add(vista)
        
        # Incrementar contador en la historia
        historia = db.query(Historia).filter(Historia.id == historia_id).first()
        if historia:
            historia.vistas_totales += 1
        
        db.commit()
        db.refresh(vista)
        
        return vista
    
    @staticmethod
    def eliminar_historia(
        db: Session,
        historia_id: int,
        usuario_id: int
    ) -> bool:
        """
        Elimina una historia (solo el dueño puede hacerlo)
        
        Args:
            db: Sesión de base de datos
            historia_id: ID de la historia
            usuario_id: ID del usuario que intenta eliminar
        
        Returns:
            True si se eliminó exitosamente
        
        Raises:
            ValueError: Si el usuario no es el dueño
            Exception: Si no existe la historia
        """
        historia = db.query(Historia).filter(Historia.id == historia_id).first()
        
        if not historia:
            raise Exception("Historia no encontrada")
        
        if historia.usuario_id != usuario_id:
            raise ValueError("No tienes permiso para eliminar esta historia")
        
        # Eliminar archivos físicos
        storage_service.eliminar_archivo(historia.url_archivo.replace(f"{settings.BASE_URL}/uploads/", ""))
        if historia.url_miniatura:
            storage_service.eliminar_archivo(historia.url_miniatura.replace(f"{settings.BASE_URL}/uploads/", ""))
        
        # Eliminar de BD (cascade eliminará vistas y reacciones)
        db.delete(historia)
        db.commit()
        
        return True
    
    @staticmethod
    def obtener_visualizadores(
        db: Session,
        historia_id: int,
        usuario_id: int
    ) -> List[dict]:
        """
        Obtiene la lista de usuarios que vieron una historia
        Solo el dueño puede ver esta información
        """
        # Verificar que el usuario sea el dueño
        historia = db.query(Historia).filter(Historia.id == historia_id).first()
        
        if not historia:
            raise Exception("Historia no encontrada")
        
        if historia.usuario_id != usuario_id:
            raise ValueError("No tienes permiso para ver esta información")
        
        # Obtener vistas con información del usuario
        vistas = db.query(
            HistoriaVista,
            Usuario.nombre,
            Usuario.apellido,
            Usuario.foto
        ).join(
            Usuario,
            HistoriaVista.usuario_id == Usuario.id
        ).filter(
            HistoriaVista.historia_id == historia_id
        ).order_by(
            HistoriaVista.fecha_vista.desc()
        ).all()
        
        visualizadores = []
        for vista, nombre, apellido, foto in vistas:
            visualizadores.append({
                "usuario_id": vista.usuario_id,
                "nombre": nombre,
                "apellido": apellido,
                "foto": foto,
                "fecha_vista": vista.fecha_vista,
                "completo": vista.completo
            })
        
        return visualizadores
    
    @staticmethod
    def verificar_vistas_usuario(
        db: Session,
        historias: List[Historia],
        usuario_id: int
    ) -> dict:
        """
        Verifica qué historias ya vio el usuario
        
        Returns:
            Diccionario con historia_id: bool
        """
        historia_ids = [h.id for h in historias]
        
        vistas = db.query(HistoriaVista.historia_id).filter(
            and_(
                HistoriaVista.historia_id.in_(historia_ids),
                HistoriaVista.usuario_id == usuario_id
            )
        ).all()
        
        vistas_dict = {h_id: False for h_id in historia_ids}
        for (h_id,) in vistas:
            vistas_dict[h_id] = True
        
        return vistas_dict


# Instancia global del servicio
historia_service = HistoriaService()
