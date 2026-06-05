from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Torneo(Base):
    """
    Configuracion de torneo para calendarizacion de partidos.
    Tabla: torneo
    """

    __tablename__ = "torneo"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=True)
    tipoDeporte = Column(String(100), nullable=True)
    estado = Column(Boolean, nullable=True)

    categorias = Column(Integer, nullable=True)
    noGrupos = Column(Integer, nullable=True)
    equiposPorgrupo = Column(Integer, nullable=True)
    parejasEnGrupos = Column(Integer, nullable=True)
    noJornadas = Column(Integer, nullable=True)
    liguilla = Column(Boolean, nullable=True)
    cantidadEquiposLiguilla = Column(Integer, nullable=True)
    aplicaPlayIn = Column(Boolean, nullable=True)

    fechaInicio = Column(String(100), nullable=True)
    fechaFin = Column(String(100), nullable=True)
    FaseGrupoFin = Column(DateTime, nullable=True)
    diasJuego = Column(String(255), nullable=True)
    horaInicioTorneo = Column(String(100), nullable=True)

    cerrarInscripciones = Column(Boolean, nullable=True)
    cerrarRegistrosPadel = Column(Boolean, nullable=True)

    preventa = Column(Float, nullable=True)
    venta = Column(Float, nullable=True)
    finPreventa = Column(String(100), nullable=True)
    tipoPago = Column(String(100), nullable=True)

    permiteEmpate = Column(Boolean, nullable=True)
    cantidadSets = Column(Integer, nullable=True)
    numeroJuegos = Column(Integer, nullable=True)
    numeroJuegosTiebreak = Column(Integer, nullable=True)
    modoDesempateScore = Column(String(100), nullable=True)
    tiempoUsoCanchas = Column(String(100), nullable=True)

    solicitarHorario = Column(Boolean, nullable=True)
    horasAntesNotificar = Column(Integer, nullable=True)

    tipoGeneracion = Column(Integer, nullable=True)
    dividirRR = Column(Boolean, nullable=True)
    noGruposRR = Column(Integer, nullable=True)

    tieneArbitraje = Column(Boolean, nullable=True)
    montoArbitraje = Column(Float, nullable=True)

    imc = Column(Float, nullable=True)
    pmr = Column(Float, nullable=True)

    finalizarTorneo = Column(Boolean, nullable=True)
    ultimaModificacion = Column(DateTime, nullable=True)
    usuarioC = Column(Integer, nullable=True)

    showWebView = Column(Boolean, nullable=True)
    urlTorneo = Column(String(500), nullable=True)

    equipos = relationship("Equipo", back_populates="torneo")
    disponibilidades_jugadores = relationship("TorneoDisponibilidadJugador", back_populates="torneo")
    jornadas = relationship("Jornadas", back_populates="torneo_rel")
