from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Any, List
from datetime import datetime
from enum import Enum


class LoginRequest(BaseModel):
    """Request para login - compatible con .NET"""
    usuario: EmailStr
    contrasena: str


class BaseResponse(BaseModel):
    """Response base - compatible con .NET"""
    respuesta: str = "OK"
    mensaje: str = ""
    data: Optional[Any] = None


class UsuarioResponse(BaseModel):
    """Response con datos del usuario"""
    id: int
    nombre: str
    apellido: Optional[str] = None
    correo: str
    telefono: Optional[str] = None
    estado: Optional[str] = None
    foto: Optional[str] = None
    origen: Optional[str] = None
    token: Optional[str] = None
    
    class Config:
        from_attributes = True


# ============================================================================
# SCHEMAS PARA HISTORIAS
# ============================================================================

class TipoHistoriaEnum(str, Enum):
    """Tipo de historia"""
    imagen = "imagen"
    video = "video"


class TipoReaccionEnum(str, Enum):
    """Tipo de reacción"""
    like = "like"
    love = "love"
    fire = "fire"
    clap = "clap"
    sad = "sad"


class HistoriaCreate(BaseModel):
    """Schema para crear una historia"""
    descripcion: Optional[str] = Field(None, max_length=500)
    duracion_segundos: Optional[int] = Field(5, ge=1, le=15, description="Duración de visualización en la app (1-15 seg)")
    destacada: bool = Field(False, description="Si es destacada, no expira en 24h")
    
    @validator('descripcion')
    def validar_descripcion(cls, v):
        if v and len(v.strip()) == 0:
            return None
        return v


class HistoriaResponse(BaseModel):
    """Response de una historia"""
    id: int
    usuario_id: int
    tipo: str
    url_archivo: str
    url_miniatura: Optional[str] = None
    descripcion: Optional[str] = None
    duracion_segundos: int
    ancho: Optional[int] = None
    alto: Optional[int] = None
    fecha_creacion: datetime
    fecha_expiracion: Optional[datetime] = None
    activa: bool
    destacada: bool
    vistas_totales: int
    visto: bool = False  # Si el usuario actual ya la vio
    
    class Config:
        from_attributes = True


class HistoriaUsuarioFeed(BaseModel):
    """Usuario con sus historias para el feed"""
    usuario_id: int
    nombre: str
    apellido: Optional[str] = None
    foto_perfil: Optional[str] = None
    tiene_historias_nuevas: bool = False
    historias: List[HistoriaResponse] = []


class HistoriaFeedResponse(BaseModel):
    """Response del feed de historias"""
    usuarios: List[HistoriaUsuarioFeed] = []
    total_usuarios: int = 0
    total_historias: int = 0


class HistoriaVistaCreate(BaseModel):
    """Schema para marcar una historia como vista"""
    tiempo_visto_segundos: Optional[int] = Field(0, ge=0)
    completo: bool = Field(True)


class HistoriaVistaResponse(BaseModel):
    """Response de una vista"""
    id: int
    historia_id: int
    usuario_id: int
    nombre_usuario: Optional[str] = None
    foto_usuario: Optional[str] = None
    fecha_vista: datetime
    completo: bool
    
    class Config:
        from_attributes = True


class HistoriaReaccionCreate(BaseModel):
    """Schema para crear una reacción"""
    tipo_reaccion: TipoReaccionEnum = TipoReaccionEnum.like


class HistoriaReaccionResponse(BaseModel):
    """Response de una reacción"""
    id: int
    historia_id: int
    usuario_id: int
    tipo_reaccion: str
    fecha_reaccion: datetime
    
    class Config:
        from_attributes = True


class MisHistoriasResponse(BaseModel):
    """Response de mis historias con estadísticas"""
    id: int
    tipo: str
    url_archivo: str
    url_miniatura: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_creacion: datetime
    fecha_expiracion: Optional[datetime] = None
    activa: bool
    destacada: bool
    vistas_totales: int
    duracion_segundos: int
    visualizadores: List[HistoriaVistaResponse] = []
    
    class Config:
        from_attributes = True
