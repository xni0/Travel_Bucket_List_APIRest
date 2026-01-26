from fastapi import FastAPI
from app.database.database import engine, Base
from app.routes import destinations, activities

# --- CREACIÓN DE TABLAS ---
# Esto revisa los modelos y crea el archivo 'travel.db' con las tablas vacías
# si no existen todavía.
Base.metadata.create_all(bind=engine)

# --- CONFIGURACIÓN DE LA APP ---
app = FastAPI(
    title="Travel Bucket List API",
    description="API con persistencia en SQLite para gestionar viajes y actividades",
    version="2.0.0"
)

# --- CONEXIÓN DE RUTAS (ROUTERS) ---
app.include_router(destinations.router)
app.include_router(activities.router)

# --- ENDPOINT DE BIENVENIDA ---
@app.get("/")
def root():
    return {
        "message": "¡Bienvenida a tu API de Viajes con Base de Datos!",
        "docs": "Ve a /docs para probar los endpoints"
    }