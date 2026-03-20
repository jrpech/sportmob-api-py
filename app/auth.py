from datetime import datetime, timedelta
from typing import Optional
import jwt
import uuid
from app.config import settings


def generate_jwt_token(user_id: int, name: str, email: str) -> str:
    """
    Genera un token JWT con la MISMA configuración que el proyecto .NET
    para asegurar compatibilidad entre ambas APIs.
    
    Claims incluidos (idénticos a .NET):
    - sub: email del usuario
    - fullName: nombre completo
    - usuario: email del usuario
    - id: ID del usuario
    - jti: GUID único
    - exp: fecha de expiración
    - iss: issuer
    - aud: audience
    """
    
    # Calcular tiempo de expiración
    expiration = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
    
    # Crear payload con los mismos claims que .NET
    payload = {
        "sub": email,
        "fullName": str(name),
        "usuario": str(email),
        "id": str(user_id),
        "jti": str(uuid.uuid4()),
        "exp": expiration,
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE
    }
    
    # Generar el token usando el mismo secret key y algoritmo
    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return token


def decode_jwt_token(token: str) -> Optional[dict]:
    """
    Decodifica y valida un token JWT.
    Compatible con tokens generados por la API .NET.
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            issuer=settings.JWT_ISSUER,
            audience=settings.JWT_AUDIENCE
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_current_user_from_token(token: str) -> Optional[dict]:
    """
    Extrae la información del usuario del token JWT
    """
    payload = decode_jwt_token(token)
    if payload is None:
        return None
    
    return {
        "id": int(payload.get("id", 0)),
        "nombre": payload.get("fullName", ""),
        "correo": payload.get("usuario", ""),
        "email": payload.get("sub", "")
    }
