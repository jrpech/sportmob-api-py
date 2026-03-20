"""
Ejemplo de router con endpoints protegidos por autenticación JWT

Este archivo muestra cómo crear endpoints que requieren autenticación.
Para usarlo:
1. Descomenta la línea en main.py para incluir este router
2. Los endpoints estarán protegidos con el token JWT
"""

from fastapi import APIRouter, Depends
from app.dependencies import get_current_user, get_current_user_optional
from app.schemas import BaseResponse
from typing import Optional

router = APIRouter(prefix="/api/User", tags=["User"])


@router.get("/perfil", response_model=BaseResponse)
async def get_perfil(current_user: dict = Depends(get_current_user)):
    """
    Endpoint protegido que retorna el perfil del usuario autenticado.
    Requiere enviar el token JWT en el header Authorization.
    
    Header requerido:
        Authorization: Bearer <token>
    """
    return BaseResponse(
        respuesta="OK",
        mensaje="",
        data={
            "usuario": current_user,
            "mensaje": f"Hola {current_user['nombre']}"
        }
    )


@router.get("/datos", response_model=BaseResponse)
async def get_datos_usuario(current_user: dict = Depends(get_current_user)):
    """
    Otro ejemplo de endpoint protegido.
    Solo usuarios autenticados pueden acceder.
    """
    return BaseResponse(
        respuesta="OK",
        mensaje="Datos del usuario",
        data={
            "id": current_user["id"],
            "nombre": current_user["nombre"],
            "correo": current_user["correo"]
        }
    )


@router.get("/publico", response_model=BaseResponse)
async def endpoint_publico(
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """
    Endpoint donde la autenticación es opcional.
    Muestra diferente información si el usuario está autenticado o no.
    """
    if current_user:
        mensaje = f"Bienvenido de vuelta, {current_user['nombre']}!"
    else:
        mensaje = "Bienvenido, invitado!"
    
    return BaseResponse(
        respuesta="OK",
        mensaje=mensaje,
        data={
            "autenticado": current_user is not None,
            "usuario": current_user
        }
    )
