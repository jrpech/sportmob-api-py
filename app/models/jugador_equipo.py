from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database import Base


class JugadorEquipo(Base):
    """
    Tabla puente entre jugador y equipo.
    Tabla: jugadorequipo
    """

    __tablename__ = "jugadorequipo"

    id = Column(Integer, primary_key=True, index=True)
    jugadorID = Column(Integer, ForeignKey("jugador.id"), nullable=False, index=True)
    equipoID = Column(Integer, ForeignKey("equipo.id"), nullable=False, index=True)

    jugador = relationship("Jugador")
    equipo = relationship("Equipo", back_populates="jugadores_equipo")
