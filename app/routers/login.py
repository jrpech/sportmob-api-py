from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Usuario
from app.schemas import LoginRequest, BaseResponse, UsuarioResponse
from app.auth import generate_jwt_token
import hashlib
import base64

router = APIRouter(prefix="/api/Login", tags=["Authentication"])


def verify_password(plain_password: str, stored_password: str) -> bool:
    """
    Verifica la contraseña según el método usado en .NET.
    
    IMPORTANTE: El código .NET compara directamente con la contraseña almacenada.
    Si las contraseñas están hasheadas en la BD, ajusta esta función.
    
    Opciones disponibles:
    1. Comparación directa (si están en texto plano)
    2. SHA1 + Base64 (como en Cifrado.cs de .NET)
    """
    
    # Opción 1: Comparación directa (si las contraseñas están en texto plano)
    if plain_password == stored_password:
        return True
    
    # Opción 2: SHA1 con Unicode encoding + Base64 (como Cifrado.cs)
    # Usar este método si las contraseñas están hasheadas
    try:
        hashed = hashlib.sha1(plain_password.encode('utf-16-le')).digest()
        hashed_b64 = base64.b64encode(hashed).decode('utf-8')
        if hashed_b64 == stored_password:
            return True
    except:
        pass
    
    return False


@router.post("/auth", response_model=BaseResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Endpoint de autenticación compatible con la API .NET.
    
    Genera un token JWT con la misma configuración que .NET para
    asegurar que la app móvil pueda usar ambas APIs indistintamente.
    """
    try:
        # Buscar usuario por correo
        usuario = db.query(Usuario).filter(
            Usuario.correo == request.usuario
        ).first()
        
        if not usuario:
            raise Exception("Usuario y/o contraseña invalidos")
        
        # Verificar contraseña
        if not verify_password(request.contrasena, usuario.contrasenia):
            raise Exception("Usuario y/o contraseña invalidos")
        
        # Generar token JWT (compatible con .NET)
        token = generate_jwt_token(
            user_id=usuario.id,
            name=usuario.nombre,
            email=usuario.correo
        )
        
        # Preparar respuesta
        usuario_data = {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "correo": usuario.correo,
            "telefono": usuario.telefono,
            "estado": usuario.estado,
            "foto": usuario.foto,
            "origen": usuario.origen,
            "token": token
        }
        
        return BaseResponse(
            respuesta="OK",
            mensaje="",
            data=usuario_data
        )
        
    except Exception as ex:
        error_mensaje = str(ex)
        if hasattr(ex, 'InnerException') and ex.InnerException:
            error_mensaje += str(ex.InnerException)
        
        return BaseResponse(
            respuesta="ERROR",
            mensaje=error_mensaje,
            data=None
        )
