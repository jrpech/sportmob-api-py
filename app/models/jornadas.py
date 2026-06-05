from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Jornadas(Base):
    """
    Modelo de jornada o fase dentro de torneo.
    Tabla: jornadas
    """

    __tablename__ = "jornadas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=True)
    fechaInicio = Column(DateTime, nullable=True)
    fechaFin = Column(DateTime, nullable=True)

    tipoJornada = Column(String(100), nullable=True)
    nombreLiguilla = Column(String(150), nullable=True)
    etapaLiguilla = Column(String(150), nullable=True)
    llaveLiguilla = Column(Integer, nullable=True)
    numeroLlave = Column(Integer, nullable=True)
    posicionLlave = Column(Integer, nullable=True)
    siguienteJornada = Column(Integer, nullable=True)

    numeroJornada = Column(String(100), nullable=True)
    jornadaFinalizada = Column(Boolean, nullable=True)

    categoria = Column(Integer, nullable=True)
    torneo = Column(Integer, ForeignKey("torneo.id"), nullable=True, index=True)

    torneoC = Column(Integer, nullable=True)
    ultimaModificacion = Column(DateTime, nullable=True)
    idUsuario = Column(Integer, nullable=True)
    usuarioC = Column(Integer, nullable=True)
    cuentaId = Column(Integer, nullable=True)

    torneo_rel = relationship("Torneo", foreign_keys=[torneo])
    partidos_jornada = relationship("PartidosJornadas", back_populates="jornada")
