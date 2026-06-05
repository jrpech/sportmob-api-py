from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Equipo(Base):
    """
    Modelo de equipo/pareja inscrita en torneo.
    Tabla: equipo
    """

    __tablename__ = "equipo"

    id = Column(Integer, primary_key=True, index=True)
    nombreEquipo = Column(String(255), nullable=True)
    alias = Column(String(255), nullable=True)
    claveEquipo = Column(String(255), nullable=True)

    Torneo = Column(Integer, ForeignKey("torneo.id"), nullable=True, index=True)
    Grupo = Column(Integer, nullable=True)
    Categoria = Column(Integer, nullable=True)

    fotoEquipo = Column(String(500), nullable=True)
    fotoEquipo2 = Column(String(500), nullable=True)
    fotoUniforme = Column(String(500), nullable=True)

    fechaRegistroEquipo = Column(DateTime, nullable=True)
    cuentaId = Column(Integer, nullable=True)

    jugadoresPagados = Column(Integer, nullable=True)
    modoPago = Column(String(100), nullable=True)
    importe = Column(Float, nullable=True)
    pagado = Column(Boolean, nullable=True)
    estadoRegistroParejas = Column(String(255), nullable=True)

    eliminado = Column(Boolean, nullable=True)
    baja = Column(Boolean, nullable=True)
    clasificado = Column(Boolean, nullable=True)

    juegosJugados = Column(Integer, nullable=True)
    juegosGanados = Column(Integer, nullable=True)
    juegosEmpatados = Column(Integer, nullable=True)
    juegosPerdidos = Column(Integer, nullable=True)
    golesAFavor = Column(Float, nullable=True)
    golesEnContra = Column(Float, nullable=True)
    diferenciaDeGoles = Column(Float, nullable=True)
    puntos = Column(Float, nullable=True)
    puntosRanking = Column(Integer, nullable=True)
    ptsExtrasOAmosnetacion = Column(Float, nullable=True)

    grupoRR = Column(Integer, nullable=True)

    ultimaModificacion = Column(DateTime, nullable=True)
    idUsuario = Column(Integer, nullable=True)
    usuarioC = Column(Integer, nullable=True)

    torneo = relationship("Torneo")
    jugadores_equipo = relationship("JugadorEquipo", back_populates="equipo", cascade="all, delete-orphan")
    partidos_local = relationship("PartidosJornadas", foreign_keys="PartidosJornadas.idEquipo1", back_populates="equipo1")
    partidos_visitante = relationship("PartidosJornadas", foreign_keys="PartidosJornadas.idEquipo2", back_populates="equipo2")
