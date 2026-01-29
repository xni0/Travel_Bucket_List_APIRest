from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine, Base
from app.routes import destinations, activities

# CREACIÓN DE TABLAS 
# Esto revisa los modelos y crea el archivo 'travel.db' con las tablas vacías
# si no existen todavía.
Base.metadata.create_all(bind=engine)

# CONFIGURACIÓN DE LA APP 
app = FastAPI(
    title="Travel Bucket List API",
    description="API con persistencia en SQLite para gestionar viajes y actividades",
    version="2.0.0"
)


# CONFIGURACIÓN DE CORS
# Esto permite que un frontend (React, Vue, etc.) se comunique con este backend
# sin que el navegador bloquee la conexión.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite conectar desde cualquier origen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CONEXIÓN DE RUTAS (ROUTERS) 
# Aquí conecto los routers de destinos y actividades a la app principal.
# Cada router maneja un conjunto de endpoints relacionados (modularidad).
app.include_router(destinations.router)
app.include_router(activities.router)

# ENDPOINT DE BIENVENIDA 
# Para ver que el servidor está corriendo correctamente.
@app.get("/")
def root():
    return {
        "message": "¡Bienvenido a tu API de Viajes con Base de Datos!",
        "docs": "Ve a /docs para probar los endpoints"
    }