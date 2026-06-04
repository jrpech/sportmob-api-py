from datetime import datetime
import enum

from sqlalchemy import BigInteger, Boolean, Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Usuario(Base):
    """
    Modelo Usuario compatible con la base de datos de .NET.
    """

    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255))
    apellido = Column(String(255))
    correo = Column(String(255), unique=True, index=True)
    contrasenia = Column(String(255))
    telefono = Column(String(50))
    estado = Column(String(100))
    foto = Column(String(500))
    origen = Column(String(100))

    historias = relationship("Historia", back_populates="usuario", cascade="all, delete-orphan")

    def dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "correo": self.correo,
            "telefono": self.telefono,
            "estado": self.estado,
            "foto": self.foto,
            "origen": self.origen,
        }


class TipoHistoria(str, enum.Enum):
    imagen = "imagen"
    video = "video"


class Historia(Base):
    """
    Modelo de Historia (Story tipo Instagram).
    """

    __tablename__ = "historia"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False, index=True)

    tipo = Column(Enum(TipoHistoria), nullable=False)

    url_archivo = Column(String(500), nullable=False)
    url_miniatura = Column(String(500))
    nombre_archivo = Column(String(255))

    descripcion = Column(Text)
    duracion_segundos = Column(Integer, default=5)

    ancho = Column(Integer)
    alto = Column(Integer)
    tamano_bytes = Column(BigInteger)
    duracion_video = Column(Integer)

    fecha_creacion = Column(DateTime, default=datetime.utcnow, index=True)
    fecha_expiracion = Column(DateTime)
    activa = Column(Boolean, default=True, index=True)

    destacada = Column(Boolean, default=False, index=True)

    vistas_totales = Column(Integer, default=0)

    usuario = relationship("Usuario", back_populates="historias")
    vistas = relationship("HistoriaVista", back_populates="historia", cascade="all, delete-orphan")
    reacciones = relationship("HistoriaReaccion", back_populates="historia", cascade="all, delete-orphan")

    def dict(self):
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
            "vistas_totales": self.vistas_totales,
        }


class HistoriaVista(Base):
    """
    Registro de visualizaciones de historias.
    """

    __tablename__ = "historia_vista"

    id = Column(Integer, primary_key=True, index=True)
    historia_id = Column(Integer, ForeignKey("historia.id", ondelete="CASCADE"), nullable=False, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    fecha_vista = Column(DateTime, default=datetime.utcnow, index=True)

    tiempo_visto_segundos = Column(Integer, default=0)
    completo = Column(Boolean, default=False)

    historia = relationship("Historia", back_populates="vistas")

    def dict(self):
        return {
            "id": self.id,
            "historia_id": self.historia_id,
            "usuario_id": self.usuario_id,
            "fecha_vista": self.fecha_vista.isoformat() if self.fecha_vista else None,
            "completo": self.completo,
        }


class TipoReaccion(str, enum.Enum):
    like = "like"
    love = "love"
    fire = "fire"
    clap = "clap"
    sad = "sad"


class HistoriaReaccion(Base):
    """
    Reacciones a historias.
    """

    __tablename__ = "historia_reaccion"

    id = Column(Integer, primary_key=True, index=True)
    historia_id = Column(Integer, ForeignKey("historia.id", ondelete="CASCADE"), nullable=False, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    tipo_reaccion = Column(Enum(TipoReaccion), default=TipoReaccion.like)
    fecha_reaccion = Column(DateTime, default=datetime.utcnow)

    historia = relationship("Historia", back_populates="reacciones")

    def dict(self):
        return {
            "id": self.id,
            "historia_id": self.historia_id,
            "usuario_id": self.usuario_id,
            "tipo_reaccion": self.tipo_reaccion.value if self.tipo_reaccion else None,
            "fecha_reaccion": self.fecha_reaccion.isoformat() if self.fecha_reaccion else None,
        }


class Cuenta(Base):
    """
    Modelo de Cuenta que se encuentran en sportmob.
    """

    __tablename__ = "cuenta"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255))
    estado = Column(Boolean, default=False)
    noEstadisticas = Column(Integer, default=0)
    token = Column(String(255), unique=True, index=True)
    mostrarEstadisticas = Column(Boolean, default=False)
    permiteRegistroJugador = Column(Boolean, default=False)
    fotoCuenta = Column(String(500))
    permitirDados = Column(Boolean, default=False)
    penalDtMomentoPartido = Column(Boolean, default=False)
    ignorarCanchasAuto = Column(Boolean, default=False)
    penalesDTSegundoTiempo = Column(Boolean, default=False)
    considerarAmarillasEsta = Column(Boolean, default=False)
    ptsVictoriaGrupo = Column(Integer, default=3)
    pts4toLugar = Column(Integer, default=0)
    pts3erLugar = Column(Integer, default=0)
    ptsFinalista = Column(Integer, default=0)
    ptsCampeon = Column(Integer, default=0)
    ptsUploadCategory = Column(Integer, default=100)
    ignorarVolado = Column(Boolean, default=False)

    def dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "noEstadisticas": self.noEstadisticas,
            "token": self.token,
            "mostrarEstadisticas": self.mostrarEstadisticas,
            "permiteRegistroJugador": self.permiteRegistroJugador,
            "fotoCuenta": self.fotoCuenta,
            "permitirDados": self.permitirDados,
            "penalDtMomentoPartido": self.penalDtMomentoPartido,
            "ignorarCanchasAuto": self.ignorarCanchasAuto,
            "penalesDTSegundoTiempo": self.penalesDTSegundoTiempo,
            "considerarAmarillasEsta": self.considerarAmarillasEsta,
            "ptsVictoriaGrupo": self.ptsVictoriaGrupo,
            "pts4toLugar": self.pts4toLugar,
            "pts3erLugar": self.pts3erLugar,
            "ptsFinalista": self.ptsFinalista,
            "ptsCampeon": self.ptsCampeon,
            "ptsUploadCategory": self.ptsUploadCategory,
            "ignorarVolado": self.ignorarVolado,
        }


class Jugador(Base):
    """
    Modelo de Jugador que se encuentran en sportmob.
    """

    __tablename__ = "jugador"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(45), nullable=True)
    apellido = Column(String(45), nullable=True)
    fechaNacimiento = Column(String(45), nullable=True)
    documento = Column(String(500), nullable=True)
    peso = Column(Float, nullable=True)
    altura = Column(Float, nullable=True)
    email = Column(String(45), nullable=True)
    telefono = Column(String(45), nullable=True)
    posicion = Column(String(45), nullable=True)
    talla = Column(String(45), nullable=True)
    noJugador = Column(Integer, nullable=True)
    nombreJersy = Column(String(45), nullable=True)
    foto = Column(String(450), nullable=True)
    equipoID = Column(Integer, nullable=True)
    equipo = Column(Integer, nullable=True)
    estado = Column(String(45), nullable=True)
    codigoPostal = Column(Integer, nullable=True)
    fechaRegistro = Column(String(500), nullable=True)
    esCapitan = Column(Boolean, nullable=True)
    diasExpulsado = Column(Integer, nullable=True)
    segfoto = Column(String(200), nullable=True)
    ultimaModificacion = Column(DateTime, nullable=True)
    idUsuario = Column(Integer, nullable=True)
    usuarioC = Column(Integer, nullable=True)
    modoPago = Column(String(20), nullable=True)
    torneoID = Column(Integer, nullable=True)
    categoriaID = Column(Integer, nullable=True)
    claveUnica = Column(String(200), nullable=True)
    importe = Column(Float, nullable=True)
    pagado = Column(Boolean, nullable=True)
    registroComo = Column(String(45), nullable=True)
    clavedeInvitacion = Column(String(45), nullable=True)
    puntosEstrella = Column(Float, nullable=True, default=0)
    puntosSemana = Column(Float, nullable=True, default=0)
    tipoDeporte = Column(String(45), nullable=True, default="FUTBOL")
    usuarioJugadorID = Column(Integer, nullable=True)
    puntosRanking = Column(Integer, nullable=True, default=0)
    refuerzo = Column(Boolean, nullable=True)
    origenEquipoRefuerzo = Column(String(250), nullable=True)
    fotoAlter = Column(String(450), nullable=True)
    genero = Column(String(450), nullable=True)
    jugadorInsignia = Column(Boolean, nullable=True)
    contrasenia = Column(String(255), nullable=True)
    origen = Column(String(100), nullable=True)


class UsuarioDispositivos(Base):
    """
    Modelo de tokens de dispositivos por usuario (Firebase).
    """

    __tablename__ = "usuario_dispositivos"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(500), nullable=False)
    usuarioID = Column(Integer, nullable=False, index=True)
    fechaRegistro = Column(DateTime, default=datetime.utcnow, nullable=False)

    def dict(self):
        return {
            "id": self.id,
            "token": self.token,
            "usuarioID": self.usuarioID,
            "fechaRegistro": self.fechaRegistro.isoformat() if self.fechaRegistro else None,
        }
