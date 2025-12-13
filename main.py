from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# MODELO DE DATOS 
class Destination(BaseModel):
    id: int
    name: str
    country: str
    budget: float
    visited: bool
    activities: List[str]

# BASE DE DATOS SIMULADA 
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
@app.get("/")
async def root():
    return {"message": "API de Gestor de Viajes funcionando"}

@app.get("/destinations/", response_model=List[Destination])
async def get_all_destinations():
    return destinations_fake_db

@app.get("/destinations/{id_destination}", response_model=Destination)
async def get_destination_by_id(id_destination: int):
    return await search_destination(id_destination)

@app.post("/destinations/", response_model=Destination, status_code=201)
async def add_destination(destination: Destination):
    if any(dest_stored.id == destination.id for dest_stored in destinations_fake_db):
        raise HTTPException(status_code=409, detail="Ese ID de destino ya está en uso")
    destinations_fake_db.append(destination)
    return destination

@app.put("/destinations/{id_destination}", response_model=Destination)
async def update_destination(id_destination: int, destination: Destination):
    for index, dest_stored in enumerate(destinations_fake_db):
        if dest_stored.id == id_destination:
            destination.id = id_destination
            destinations_fake_db[index] = destination
            return destination
    raise HTTPException(status_code=404, detail=f"Destino con id {id_destination} no encontrado")

@app.delete("/destinations/{id_destination}")
async def delete_destination(id_destination: int):
    for index, dest_stored in enumerate(destinations_fake_db):
        if dest_stored.id == id_destination:
            destinations_fake_db.pop(index)
            return {"message": f"Destino con id {id_destination} eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Destino no encontrado")

async def search_destination(id: int):
    for dest in destinations_fake_db:
        if dest.id == id:
            return dest
    raise HTTPException(status_code=404, detail="Destino no encontrado")