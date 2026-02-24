import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# CARGA DE VARIABLES DE ENTORNO
# Busca el archivo .env en mi raíz para cargar credenciales de forma segura
load_dotenv()

# Obtiene la URL de la base de datos (local o de Render)
DATABASE_URL = os.getenv("DATABASE_URL")

# COMPATIBILIDAD CON RENDER / POSTGRES
# SQLAlchemy requiere que el protocolo sea 'postgresql://'. 
# Si Render nos da 'postgres://', lo corregimos automáticamente.
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Validación de seguridad: si no hay URL, la aplicación no debe arrancar
if not DATABASE_URL:
    raise ValueError("ERROR: La variable de entorno DATABASE_URL no está configurada.")

# CONFIGURACIÓN DEL MOTOR (ENGINE)
# Es el encargado de gestionar la comunicación física con PostgreSQL
engine = create_engine(DATABASE_URL)

# CONFIGURACIÓN DE LA SESIÓN (SESSIONMAKER)
# Crea una "fábrica" de sesiones para realizar operaciones (CRUD) en la DB.
# autocommit/autoflush=False nos da control total sobre cuándo guardar los datos.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# CLASE BASE DECLARATIVA
# Clase maestra de la que heredarán todos nuestros modelos (Destination, Activity).
# Permite que SQLAlchemy mapee nuestras clases de Python a tablas de la DB.
Base = declarative_base()

# DEPENDENCIA PARA LA INYECCIÓN (Dependency Injection)
# Función para obtener una conexión a la base de datos en cada petición.
def get_db():
    db = SessionLocal() # Crea una nueva sesión
    try:
        yield db       # Entrega la sesión a la ruta que la pidió
    finally:
        db.close()     # GARANTÍA: La conexión se cierra siempre al terminar,
                       # evitando saturar la base de datos con conexiones huérfanas.