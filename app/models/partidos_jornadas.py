from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class PartidosJornadas(Base):
    """
    Modelo de partido programado entre dos equipos.
    Tabla: partidosjornadas
    """

    __tablename__ = "partidosjornadas"

    id = Column(Integer, primary_key=True, index=True)

    idJornada = Column(Integer, ForeignKey("jornadas.id"), nullable=True, index=True)

    idEquipo1 = Column(Integer, ForeignKey("equipo.id"), nullable=True, index=True)
    idEquipo2 = Column(Integer, ForeignKey("equipo.id"), nullable=True, index=True)
    grupoID = Column(Integer, nullable=True)

    fechaHoraPartido = Column(DateTime, nullable=True)
    hora = Column(String(100), nullable=True)
    lugar = Column(Integer, nullable=True)
    etiquetaCancha = Column(String(255), nullable=True)

    marcadorEquipo1 = Column(Integer, nullable=True)
    marcadorEquipo2 = Column(Integer, nullable=True)
    estadoPartido = Column(String(100), nullable=True)

    tipoPartido = Column(String(100), nullable=True)
    partidoSugerido = Column(Boolean, nullable=True)
    modificadoManual = Column(Boolean, nullable=True)
    currentStatePadel = Column(String(100), nullable=True)

    jornada = relationship("Jornadas", back_populates="partidos_jornada")
    equipo1 = relationship("Equipo", foreign_keys=[idEquipo1], back_populates="partidos_local")
    equipo2 = relationship("Equipo", foreign_keys=[idEquipo2], back_populates="partidos_visitante")
