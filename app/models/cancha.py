from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Cancha(Base):
    """
    Modelo de cancha disponible para calendarizacion.
    Tabla: cancha
    """

    __tablename__ = "cancha"

    ID = Column(Integer, primary_key=True, index=True)
    nombreCancha = Column(String(45), nullable=True)
    ubicacionCancha = Column(String(100), nullable=True)
    estadoCancha = Column(Boolean, nullable=True)
    ultimaModificacion = Column(DateTime, nullable=True)
    idUsuario = Column(Integer, nullable=True)
    usuarioC = Column(Integer, nullable=True)
    cuentaId = Column(Integer, nullable=True)
    fechas = Column(Integer, nullable=True)

    dias = relationship("Fechas", back_populates="cancha", cascade="all, delete-orphan")
