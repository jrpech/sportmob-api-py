from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class TorneoDisponibilidadJugador(Base):
    """
    Disponibilidad horaria declarada por jugador para un torneo.
    Tabla: TorneoDisponibilidadJugador
    """

    __tablename__ = "TorneoDisponibilidadJugador"
    __table_args__ = (
        Index("idx_torneo", "idTorneo"),
        Index("idx_jugador", "idJugador"),
        Index("idx_torneo_jugador", "idTorneo", "idJugador"),
    )

    id = Column(Integer, primary_key=True, index=True)
    idTorneo = Column(Integer, ForeignKey("torneo.id"), nullable=False, index=True)
    idJugador = Column(Integer, ForeignKey("jugador.id"), nullable=False, index=True)
    fecha = Column(DateTime, nullable=False)
    hora = Column(String(50), nullable=True)
    alta = Column(DateTime, nullable=True)

    torneo = relationship("Torneo", back_populates="disponibilidades_jugadores")
    jugador = relationship("Jugador")
