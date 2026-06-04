from sqlalchemy import Column, Integer

from app.database import Base


class CuentaTorneo(Base):
    """
    Relacion entre cuenta y torneo.
    Tabla: cuentatorneo
    """

    __tablename__ = "cuentatorneo"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    torneo = Column(Integer, nullable=True)
    cuentaId = Column(Integer, nullable=True)
