import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv

# --- MEJORA: CARGA DE ENTORNOS ---
# Cargamos las variables de entorno para que Alembic conozca la DATABASE_URL
load_dotenv()

# --- MEJORA: IMPORTACIÓN DE MODELOS ---
# Importamos la Base y los modelos para que Alembic detecte los cambios en las tablas
from app.database.database import Base
# Importar aquí todos tus modelos para que se registren en Base.metadata
from app.models.models import Destination, Activity 

# Objeto de configuración de Alembic
config = context.config

# Configuración de logs
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- MEJORA: METADATA PARA AUTOGENERATE ---
target_metadata = Base.metadata

def get_url():
    """Obtiene la URL de la base de datos y corrige el prefijo de Render si es necesario."""
    url = os.getenv("DATABASE_URL")
    if url and url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url

def run_migrations_offline() -> None:
    """Modo offline: se usa la URL de la variable de entorno."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Modo online: se crea el motor de SQLAlchemy con la URL dinámica."""
    # Obtenemos la sección de configuración y sobrescribimos la URL
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()