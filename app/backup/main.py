from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel
from typing import List

app = FastAPI()


# CONFIGURACIÓN DE CORS (AÑADIDO PARA LA PRÁCTICA DE REACT)
# Esto permite que mi frontend en el puerto 5173 hable con este backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite conectar desde cualquier origen (ej: localhost:5173)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],
)


# SECCIÓN USUARIOS (AÑADIDO PARA LA PRÁCTICA DE REACT)

# Modelo de Usuario
class User(BaseModel):
    id: int
    name: str
    surname: str
    email: str

# Base de datos simulada de usuarios
users_fake_db = [
    User(id=1, name="Vicent", surname="Foo", email="vicent@example.com"),
    User(id=2, name="Lucilene", surname="Bar", email="lucilene@example.com"),
    User(id=3, name="Pepe", surname="Gotera", email="pepe@example.com"),
]

# Endpoint para obtener usuarios (Lo que pide tu práctica de React)
@app.get("/users", response_model=List[User])
def get_users():
    return users_fake_db

# SECCIÓN DESTINOS (TU CÓDIGO ORIGINAL CON TUS COMENTARIOS)

# MODELO DE DATOS 
# Sirve para validar y estructurar los datos de los destinos
# Cada destino tiene un id, nombre, país, presupuesto, estado de visita y lista de actividades
class Destination(BaseModel):
    id: int
    name: str
    country: str
    budget: float
    visited: bool
    activities: List[str] # Lista de actividades como strings
                          # No es una entidad propia en esta versión simple

# BASE DE DATOS SIMULADA 
# Es volátil: se pierde al reiniciar el servidor
# Es una lista que vive en la RAM del ordenador
destinations_fake_db = [
    Destination(id=1, name="Tokio", country="Japon", budget=2500.0, visited=False, activities=["Torre de Tokio", "Shibuya", "Cruce peatonal"]),
    Destination(id=2, name="Paris", country="Francia", budget=1200.50, visited=True, activities=["Torre Eiffel", "Louvre", "Arco del Triunfo"]),
    Destination(id=3, name="Nueva York", country="USA", budget=3000.0, visited=False, activities=["Central Park", "Estatua de la Libertad", "Times Square"]),
    Destination(id=4, name="Roma", country="Italia", budget=1500.0, visited=True, activities=["Coliseo", "Vaticano", "Fontana di Trevi"]),
    Destination(id=5, name="Rio de Janeiro", country="Brasil", budget=2200.0, visited=False, activities=["Cristo Redentor", "Copacabana", "Pan de Azúcar"]),
    Destination(id=6, name="Sidney", country="Australia", budget=3500.0, visited=False, activities=["Opera House", "Bondi Beach", "Harbour Bridge"]),
    Destination(id=7, name="Machu Picchu", country="Peru", budget=1800.0, visited=True, activities=["Ruta Inca", "Templo del Sol", "Ver llamas"]),
    Destination(id=8, name="El Cairo", country="Egipto", budget=1100.0, visited=False, activities=["Pirámides de Giza", "Esfinge", "Museo Egipcio"]),
]

# ENDOPOINTS DE LA API
# Como no hay base de datos real lo unico que se hace es manipular una lista en memoria
@app.get("/")
async def root():
    return {"message": "API de Gestor de Viajes funcionando"}

# Endpoint para obtener todos los destinos
# response_model indica el schema para formatear la respuesta
@app.get("/destinations/", response_model=List[Destination])
def get_all_destinations():
    return destinations_fake_db

# Endpoint para obtener un destino por su ID
# response_model indica el schema para formatear la respuesta
@app.get("/destinations/{id_destination}", response_model=Destination)
def get_destination_by_id(id_destination: int):
    # Reutilizo la función auxiliar para buscar el destino
    return search_destination(id_destination)

# Endpoint para crear un nuevo destino
# response_model indica el schema para formatear la respuesta
@app.post("/destinations/", response_model=Destination, status_code=201)
def add_destination(destination: Destination):
    if any(dest_stored.id == destination.id for dest_stored in destinations_fake_db):
        raise HTTPException(status_code=409, detail="Ese ID de destino ya está en uso")
    # Agrego el nuevo destino a la "base de datos"
    destinations_fake_db.append(destination)
    return destination

# Endpoint para actualizar un destino existente
# response_model indica el schema para formatear la respuesta
@app.put("/destinations/{id_destination}", response_model=Destination)
def update_destination(id_destination: int, destination: Destination):
    # Busco el destino por ID y lo actualizo
    # recorro la lista de destinos
    # uso enumarate para obtener el índice en la lista 
    # ya que necesito reemplazar el objeto completo, no solo modificarlo
    # si usara for dest in destinations_fake_db: no tendría forma de saber el índice
    for index, dest_stored in enumerate(destinations_fake_db):
        if dest_stored.id == id_destination:
            # para mantener el mismo ID
            destination.id = id_destination
            # reemplazo el destino en la lista
            destinations_fake_db[index] = destination
            return destination
    raise HTTPException(status_code=404, detail=f"Destino con id {id_destination} no encontrado")

# Endpoint para eliminar un destino por su ID
@app.delete("/destinations/{id_destination}")
def delete_destination(id_destination: int):
    # Recorro la lista de destinos para encontrar el que coincida con el ID
    # uso enumerate para obtener el índice y poder eliminarlo
    for index, dest_stored in enumerate(destinations_fake_db):
        if dest_stored.id == id_destination:
            # elimino el destino de la lista
            # hago .pop para eliminar por índice
            destinations_fake_db.pop(index)
            return {"message": f"Destino con id {id_destination} eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Destino no encontrado")

# Función auxiliar para buscar un destino por ID
def search_destination(id: int):
    # Recorro la lista de destinos buscando el ID
    for dest in destinations_fake_db:
        if dest.id == id:
            return dest
    raise HTTPException(status_code=404, detail="Destino no encontrado")