from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Horarios(Base):
    """
    Modelo de horarios disponibles por dia.
    Tabla: horarios
    """

    __tablename__ = "horarios"

    id = Column(Integer, primary_key=True, index=True)
    horario = Column(String(150), nullable=True)
    fechaID = Column(Integer, ForeignKey("fechas.id"), nullable=True, index=True)

    fecha = relationship("Fechas", back_populates="bloques_horarios")
