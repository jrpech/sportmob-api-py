from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum


class Usuario(Base):
    """
    Modelo Usuario compatible con la base de datos de .NET
    """
    __tablename__ = "usuario"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255))
    apellido = Column(String(255))
    correo = Column(String(255), unique=True, index=True)
    contrasenia = Column(String(255))  # Nombre igual que en .NET
    telefono = Column(String(50))
    estado = Column(String(100))
    foto = Column(String(500))
    origen = Column(String(100))
    
    # Relaciones
    historias = relationship("Historia", back_populates="usuario", cascade="all, delete-orphan")
    
    def dict(self):
        """Convertir el modelo a diccionario sin la contraseña"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "correo": self.correo,
            "telefono": self.telefono,
            "estado": self.estado,
            "foto": self.foto,
            "origen": self.origen
        }


class TipoHistoria(str, enum.Enum):
    """Enum para tipo de historia"""
    imagen = "imagen"
    video = "video"


class Historia(Base):
    """
    Modelo de Historia (Story tipo Instagram)
    """
    __tablename__ = "historia"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Tipo de contenido
    tipo = Column(Enum(TipoHistoria), nullable=False)
    
    # URLs de archivos
    url_archivo = Column(String(500), nullable=False)
    url_miniatura = Column(String(500))
    nombre_archivo = Column(String(255))
    
    # Contenido
    descripcion = Column(Text)
    duracion_segundos = Column(Integer, default=5)  # Duración en la app
    
    # Metadata del archivo
    ancho = Column(Integer)
    alto = Column(Integer)
    tamano_bytes = Column(BigInteger)
    duracion_video = Column(Integer)  # Para videos, en segundos
    
    # Temporalidad
    fecha_creacion = Column(DateTime, default=datetime.utcnow, index=True)
    fecha_expiracion = Column(DateTime)  # NULL si es destacada
    activa = Column(Boolean, default=True, index=True)
    
    # Feature especial: Destacada (no expira)
    destacada = Column(Boolean, default=False, index=True)
    
    # Estadísticas
    vistas_totales = Column(Integer, default=0)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="historias")
    vistas = relationship("HistoriaVista", back_populates="historia", cascade="all, delete-orphan")
    reacciones = relationship("HistoriaReaccion", back_populates="historia", cascade="all, delete-orphan")
    
    def dict(self):
        """Convertir a diccionario"""
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "tipo": self.tipo.value if self.tipo else None,
            "url_archivo": self.url_archivo,
            "url_miniatura": self.url_miniatura,
            "descripcion": self.descripcion,
            "duracion_segundos": self.duracion_segundos,
            "ancho": self.ancho,
            "alto": self.alto,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "fecha_expiracion": self.fecha_expiracion.isoformat() if self.fecha_expiracion else None,
            "activa": self.activa,
            "destacada": self.destacada,
            "vistas_totales": self.vistas_totales
        }


class HistoriaVista(Base):
    """
    Registro de visualizaciones de historias
    """
    __tablename__ = "historia_vista"
    
    id = Column(Integer, primary_key=True, index=True)
    historia_id = Column(Integer, ForeignKey("historia.id", ondelete="CASCADE"), nullable=False, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    fecha_vista = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Analytics
    tiempo_visto_segundos = Column(Integer, default=0)
    completo = Column(Boolean, default=False)
    
    # Relaciones
    historia = relationship("Historia", back_populates="vistas")
    
    def dict(self):
        return {
            "id": self.id,
            "historia_id": self.historia_id,
            "usuario_id": self.usuario_id,
            "fecha_vista": self.fecha_vista.isoformat() if self.fecha_vista else None,
            "completo": self.completo
        }


class TipoReaccion(str, enum.Enum):
    """Enum para tipo de reacción"""
    like = "like"
    love = "love"
    fire = "fire"
    clap = "clap"
    sad = "sad"


class HistoriaReaccion(Base):
    """
    Reacciones a historias
    """
    __tablename__ = "historia_reaccion"
    
    id = Column(Integer, primary_key=True, index=True)
    historia_id = Column(Integer, ForeignKey("historia.id", ondelete="CASCADE"), nullable=False, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    tipo_reaccion = Column(Enum(TipoReaccion), default=TipoReaccion.like)
    fecha_reaccion = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    historia = relationship("Historia", back_populates="reacciones")
    
    def dict(self):
        return {
            "id": self.id,
            "historia_id": self.historia_id,
            "usuario_id": self.usuario_id,
            "tipo_reaccion": self.tipo_reaccion.value if self.tipo_reaccion else None,
            "fecha_reaccion": self.fecha_reaccion.isoformat() if self.fecha_reaccion else None
        }
