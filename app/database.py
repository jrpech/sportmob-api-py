from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Crear engine de SQLAlchemy
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.DEBUG
)

# Crear SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class para los modelos
Base = declarative_base()


def get_db():
    """
    Dependency para obtener la sesión de base de datos
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
