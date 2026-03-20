from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from app.auth import get_current_user_from_token

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Dependency para proteger endpoints que requieren autenticación.
    
    Uso:
        @router.get("/protected")
        async def protected_endpoint(current_user: dict = Depends(get_current_user)):
            return {"message": f"Hola {current_user['nombre']}"}
    """
    token = credentials.credentials
    user = get_current_user_from_token(token)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
) -> Optional[dict]:
    """
    Dependency para endpoints donde la autenticación es opcional.
    
    Uso:
        @router.get("/endpoint")
        async def endpoint(current_user: Optional[dict] = Depends(get_current_user_optional)):
            if current_user:
                return {"message": f"Hola {current_user['nombre']}"}
            else:
                return {"message": "Hola invitado"}
    """
    if credentials is None:
        return None
    
    token = credentials.credentials
    return get_current_user_from_token(token)
