from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware # <--- NECESARIO PARA REACT
from pydantic import BaseModel
from typing import List, Optional

# Importaciones de tu estructura modular
from app.database.database import engine, Base
from app.routes import destinations, activities

# CREACIÓN DE TABLAS 
# Esto revisa los modelos y crea el archivo 'travel.db' con las tablas vacías
# si no existen todavía.
Base.metadata.create_all(bind=engine)

# CONFIGURACIÓN DE LA APP 
# Aquí configuro la app FastAPI y conecto los routers
# Definición de la app FastAPI con metadatos
app = FastAPI(
    title="Travel Bucket List API",
    description="API con persistencia en SQLite para gestionar viajes y actividades",
    version="2.0.0"
)

# =================================================================
# 1. CONFIGURACIÓN DE CORS (AÑADIDO PARA QUE REACT NO FALLE)
# =================================================================
# Sin esto, el navegador bloquea la conexión entre el puerto 5173 y el 8000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite conectar desde cualquier origen (ej: localhost:5173)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CONEXIÓN DE RUTAS (ROUTERS) 
# Aquí conecto los routers de destinos y actividades a la app principal
# Cada router maneja un conjunto de endpoints relacionados
app.include_router(destinations.router)
app.include_router(activities.router)

# =================================================================
# 2. ZONA DE USUARIOS (SIMULADA EN MEMORIA PARA LA PRÁCTICA)
# =================================================================
# Esto es necesario porque tu práctica de React pide /users, 
# pero tu base de datos SQL solo tenía destinations/activities.

class User(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    age: Optional[int] = None # Añado esto por si el profe lo pide

users_fake_db = [
    User(id=1, name="Vicent", surname="Foo", email="vicent@example.com", age=30),
    User(id=2, name="Lucilene", surname="Bar", email="lucilene@example.com", age=25),
    User(id=3, name="Pepe", surname="Gotera", email="pepe@example.com", age=40),
]

# Endpoint para la lista de usuarios
@app.get("/users", response_model=List[User], tags=["Users"])
def get_users():
    return users_fake_db

# Endpoint para el detalle de usuario (Necesario para UserDetail.tsx)
@app.get("/users/{user_id}", response_model=User, tags=["Users"])
def get_user(user_id: int):
    for user in users_fake_db:
        if user.id == user_id:
            return user
    return None # O lanzar HTTPException 404 si prefieres

# 1. Modifica el modelo User para que age sea opcional (si no lo hiciste antes)
class User(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    age: Optional[int] = None 

# 2. Endpoint para CREAR un usuario (POST)
@app.post("/users", response_model=User, tags=["Users"], status_code=201)
def create_user(user: User):
    # Simulamos un ID autoincremental
    new_id = len(users_fake_db) + 1
    user.id = new_id
    users_fake_db.append(user)
    return user

# =================================================================

# ENDPOINT DE BIENVENIDA 
# Para ver que el servidor está corriendo
@app.get("/")
def root():
    return {
        "message": "¡Bienvenido a tu API de Viajes con Base de Datos!",
        "docs": "Ve a /docs para probar los endpoints"
    }
