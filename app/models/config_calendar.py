from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class ConfigCalendar(Base):
    """
    Tabla puente donde se hospedan la configuracion del calendario
    aqui podemos saber los torneos involucrados
    Tabla: config_calendar
    """

    __tablename__ = "config_calendar"

    id = Column(Integer, primary_key=True, index=True)
    tournaments = Column(String(5000), nullable=False)
    description = Column(String(5000), nullable=False)
    cuentaID = Column(Integer, nullable=False)