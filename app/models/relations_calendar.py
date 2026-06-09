from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class RelationsCalendar(Base):
    """
    Tabla puente donde se hospedan, las fechas, las canchas y horarios disponibles para el universo de partidos
    Tabla: relations_calendar
    """

    __tablename__ = "relations_calendar"

    id = Column(Integer, primary_key=True, index=True)
    calendarID = Column(Integer, nullable=False)
    fecha = Column(DateTime, nullable=False)
    canchaID = Column(Integer, nullable=False)
    hora = Column(String(45), nullable=False)
    partidoID = Column(Integer, nullable=True)
