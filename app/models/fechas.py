from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Fechas(Base):
    """
    Modelo de dias disponibles por cancha.
    Tabla: fechas
    """

    __tablename__ = "fechas"

    id = Column(Integer, primary_key=True, index=True)
    dia = Column(String(150), nullable=True)
    horarios = Column(Integer, nullable=True)
    categoriaID = Column(Integer, nullable=True)
    canchaID = Column(Integer, ForeignKey("cancha.ID"), nullable=True, index=True)

    cancha = relationship("Cancha", back_populates="dias")
    #bloques_horarios = relationship("Horarios", back_populates="fecha", cascade="all, delete-orphan")
