from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Conexión a la base de datos SQLite

# Nombre de la base de datos física
SQLALCHEMY_DATABASE_URL = "sqlite:///./travel.db"

# connect_args es necesario solo para SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependencia para obtener la sesión en cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()