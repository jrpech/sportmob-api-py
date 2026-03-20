"""
Router de Historias (Stories tipo Instagram)
"""
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Historia, Usuario
from app.schemas import (
    BaseResponse,
    HistoriaCreate,
    HistoriaResponse,
    HistoriaFeedResponse,
    HistoriaUsuarioFeed,
    HistoriaVistaCreate,
    MisHistoriasResponse,
    HistoriaVistaResponse
)
from app.services.historia_service import historia_service

router = APIRouter(prefix="/api/Historia", tags=["Historias"])


@router.post("/crear", response_model=BaseResponse)
async def crear_historia(
    archivo: UploadFile = File(..., description="Imagen o video de la historia"),
    descripcion: Optional[str] = Form(None, max_length=500),
    duracion_segundos: int = Form(5, ge=1, le=15),
    destacada: bool = Form(False, description="Si es destacada, no expira en 24h"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crea una nueva historia.
    
    - **archivo**: Imagen (JPG, PNG, GIF, WEBP) o Video (MP4, MOV, AVI, WEBM)
    - **descripcion**: Texto opcional (máx 500 caracteres)
    - **duracion_segundos**: Duración de visualización en la app (1-15 segundos)
    - **destacada**: Si es destacada, se mantiene y no expira en 24h
    
    Requiere autenticación JWT.
    """
    try:
        # Validar tipo de archivo
        if not archivo.content_type:
            raise ValueError("Tipo de archivo no especificado")
        
        # Crear datos de historia
        data = HistoriaCreate(
            descripcion=descripcion,
            duracion_segundos=duracion_segundos,
            destacada=destacada
        )
        
        # Crear historia
        historia = await historia_service.crear_historia(
            db=db,
            usuario_id=current_user["id"],
            archivo=archivo,
            data=data
        )
        
        return BaseResponse(
            respuesta="OK",
            mensaje="Historia creada exitosamente",
            data={
                "id": historia.id,
                "tipo": historia.tipo.value,
                "url_archivo": historia.url_archivo,
                "url_miniatura": historia.url_miniatura,
                "descripcion": historia.descripcion,
                "duracion_segundos": historia.duracion_segundos,
                "fecha_creacion": historia.fecha_creacion.isoformat(),
                "fecha_expiracion": historia.fecha_expiracion.isoformat() if historia.fecha_expiracion else None,
                "destacada": historia.destacada,
                "vistas_totales": historia.vistas_totales
            }
        )
    
    except ValueError as e:
        return BaseResponse(
            respuesta="ERROR",
            mensaje=str(e),
            data=None
        )
    except Exception as e:
        return BaseResponse(
            respuesta="ERROR",
            mensaje=f"Error creando historia: {str(e)}",
            data=None
        )


@router.get("/feed", response_model=BaseResponse)
async def obtener_feed(
    limite: int = 50,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene el feed de historias.
    
    Retorna las historias agrupadas por usuario, ordenadas por más recientes primero.
    Marca cuáles ya fueron vistas por el usuario actual.
    
    **Query Params:**
    - `limite`: Número máximo de usuarios con historias a retornar (default: 50)
    """
    try:
        # Obtener todas las historias activas
        historias = historia_service.obtener_historias_activas(db)
        
        # Verificar cuáles ya vio el usuario
        vistas_dict = historia_service.verificar_vistas_usuario(
            db, historias, current_user["id"]
        )
        
        # Agrupar por usuario
        usuarios_dict = {}
        
        for historia in historias:
            if historia.usuario_id not in usuarios_dict:
                # Obtener datos del usuario
                usuario = db.query(Usuario).filter(Usuario.id == historia.usuario_id).first()
                if not usuario:
                    continue
                
                usuarios_dict[historia.usuario_id] = {
                    "usuario_id": usuario.id,
                    "nombre": usuario.nombre,
                    "apellido": usuario.apellido,
                    "foto_perfil": usuario.foto,
                    "tiene_historias_nuevas": False,
                    "historias": []
                }
            
            # Agregar historia
            historia_data = HistoriaResponse(
                id=historia.id,
                usuario_id=historia.usuario_id,
                tipo=historia.tipo.value,
                url_archivo=historia.url_archivo,
                url_miniatura=historia.url_miniatura,
                descripcion=historia.descripcion,
                duracion_segundos=historia.duracion_segundos,
                ancho=historia.ancho,
                alto=historia.alto,
                fecha_creacion=historia.fecha_creacion,
                fecha_expiracion=historia.fecha_expiracion,
                activa=historia.activa,
                destacada=historia.destacada,
                vistas_totales=historia.vistas_totales,
                visto=vistas_dict.get(historia.id, False)
            )
            
            usuarios_dict[historia.usuario_id]["historias"].append(historia_data)
            
            # Marcar si tiene historias nuevas
            if not vistas_dict.get(historia.id, False):
                usuarios_dict[historia.usuario_id]["tiene_historias_nuevas"] = True
        
        # Convertir a lista y limitar
        usuarios_list = list(usuarios_dict.values())[:limite]
        
        # Ordenar: usuarios con historias nuevas primero
        usuarios_list.sort(key=lambda x: (not x["tiene_historias_nuevas"], x["usuario_id"]))
        
        feed = HistoriaFeedResponse(
            usuarios=usuarios_list,
            total_usuarios=len(usuarios_list),
            total_historias=len(historias)
        )
        
        return BaseResponse(
            respuesta="OK",
            mensaje="",
            data=feed.dict()
        )
    
    except Exception as e:
        return BaseResponse(
            respuesta="ERROR",
            mensaje=f"Error obteniendo feed: {str(e)}",
            data=None
        )


@router.get("/mis-historias", response_model=BaseResponse)
async def obtener_mis_historias(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene las historias del usuario autenticado con estadísticas.
    
    Incluye:
    - Lista de historias (activas y destacadas)
    - Información de quién vio cada historia
    - Estadísticas de vistas
    """
    try:
        # Obtener historias del usuario
        historias = historia_service.obtener_historias_usuario(
            db, current_user["id"], solo_activas=True
        )
        
        resultado = []
        
        for historia in historias:
            # Obtener visualizadores
            visualizadores = historia_service.obtener_visualizadores(
                db, historia.id, current_user["id"]
            )
            
            visualizadores_data = [
                HistoriaVistaResponse(
                    id=0,  # No necesitamos el ID aquí
                    historia_id=historia.id,
                    usuario_id=v["usuario_id"],
                    nombre_usuario=f"{v['nombre']} {v.get('apellido', '')}".strip(),
                    foto_usuario=v.get("foto"),
                    fecha_vista=v["fecha_vista"],
                    completo=v["completo"]
                )
                for v in visualizadores
            ]
            
            historia_data = MisHistoriasResponse(
                id=historia.id,
                tipo=historia.tipo.value,
                url_archivo=historia.url_archivo,
                url_miniatura=historia.url_miniatura,
                descripcion=historia.descripcion,
                fecha_creacion=historia.fecha_creacion,
                fecha_expiracion=historia.fecha_expiracion,
                activa=historia.activa,
                destacada=historia.destacada,
                vistas_totales=historia.vistas_totales,
                duracion_segundos=historia.duracion_segundos,
                visualizadores=visualizadores_data
            )
            
            resultado.append(historia_data.dict())
        
        return BaseResponse(
            respuesta="OK",
            mensaje="",
            data=resultado
        )
    
    except Exception as e:
        return BaseResponse(
            respuesta="ERROR",
            mensaje=f"Error obteniendo tus historias: {str(e)}",
            data=None
        )


@router.post("/{historia_id}/ver", response_model=BaseResponse)
async def marcar_como_vista(
    historia_id: int,
    data: HistoriaVistaCreate = HistoriaVistaCreate(),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Marca una historia como vista.
    
    Registra que el usuario actual vio la historia e incrementa el contador.
    
    **Body:**
    - `tiempo_visto_segundos`: Cuántos segundos vio el usuario (opcional)
    - `completo`: Si vio la historia completa (default: true)
    """
    try:
        # Verificar que la historia existe
        historia = db.query(Historia).filter(Historia.id == historia_id).first()
        if not historia:
            raise Exception("Historia no encontrada")
        
        # No marcar como vista si es del mismo usuario
        if historia.usuario_id == current_user["id"]:
            return BaseResponse(
                respuesta="OK",
                mensaje="No se registra vista de tu propia historia",
                data=None
            )
        
        # Marcar como vista
        vista = historia_service.marcar_como_vista(
            db=db,
            historia_id=historia_id,
            usuario_id=current_user["id"],
            tiempo_visto=data.tiempo_visto_segundos,
            completo=data.completo
        )
        
        return BaseResponse(
            respuesta="OK",
            mensaje="Vista registrada",
            data={
                "historia_id": historia_id,
                "visto": True,
                "fecha_vista": vista.fecha_vista.isoformat()
            }
        )
    
    except Exception as e:
        return BaseResponse(
            respuesta="ERROR",
            mensaje=str(e),
            data=None
        )


@router.delete("/{historia_id}", response_model=BaseResponse)
async def eliminar_historia(
    historia_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Elimina una historia.
    
    Solo el dueño de la historia puede eliminarla.
    """
    try:
        historia_service.eliminar_historia(
            db=db,
            historia_id=historia_id,
            usuario_id=current_user["id"]
        )
        
        return BaseResponse(
            respuesta="OK",
            mensaje="Historia eliminada exitosamente",
            data=None
        )
    
    except ValueError as e:
        return BaseResponse(
            respuesta="ERROR",
            mensaje=str(e),
            data=None
        )
    except Exception as e:
        return BaseResponse(
            respuesta="ERROR",
            mensaje=f"Error eliminando historia: {str(e)}",
            data=None
        )


@router.get("/{historia_id}/vistas", response_model=BaseResponse)
async def obtener_vistas_historia(
    historia_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene la lista de usuarios que vieron una historia.
    
    Solo el dueño de la historia puede ver esta información.
    """
    try:
        visualizadores = historia_service.obtener_visualizadores(
            db=db,
            historia_id=historia_id,
            usuario_id=current_user["id"]
        )
        
        return BaseResponse(
            respuesta="OK",
            mensaje="",
            data={
                "historia_id": historia_id,
                "total_vistas": len(visualizadores),
                "visualizadores": visualizadores
            }
        )
    
    except ValueError as e:
        return BaseResponse(
            respuesta="ERROR",
            mensaje=str(e),
            data=None
        )
    except Exception as e:
        return BaseResponse(
            respuesta="ERROR",
            mensaje=f"Error obteniendo vistas: {str(e)}",
            data=None
        )
