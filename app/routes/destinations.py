from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.models.models import Destination
from app.schemas import schemas
from app.models import models  

# Aqui conecto las peticiones del usuario HTTP con la base de datos (SQLAlchemy)

# Definición del router para destinos
# Sirve para agrupar endpoints relacionados
router = APIRouter(
    prefix="/destinations", # Ruta base para todos los endpoints de destinos
    tags=["Destinations"] # Etiqueta para agrupar en la documentación
)

# Endpoint para obtener todos los destinos (con paginación opcional)
@router.get("/", response_model=List[schemas.DestinationResponse]) # Para devolver una lista de destinos formateados 
                                                                   # según el schema DestinationResponse
# Paginación con skip y limit
# skip: cuántos registros saltarse (por defecto 0)
# limit: cuántos registros devolver como máximo (por defecto 100)
def get_destinations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Consulta a la base de datos con paginación
    # Es como hacer SELECT * FROM destinations OFFSET skip LIMIT limit
    # .all devuelve todos los resultados como una lista
    return db.query(models.Destination).offset(skip).limit(limit).all()

# Endpoint para obtener un destino por su ID
# parametro response_model indica el schema para formatear la respuesta
# FastAPI coge el objeto de la BD y lo convierte en formato JSON según el schema
@router.get("/{destination_id}", response_model=schemas.DestinationResponse)
# db: Session = Depends(get_db) --> Inyección de dependencia para obtener la sesión de BD
def get_destination(destination_id: int, db: Session = Depends(get_db)):
    # Consulta a la base de datos para buscar el destino por ID
    # Es como hacer SELECT * FROM destinations WHERE id = [numero] LIMIT 1;
    # Si no lo encuentra, devuelve 404
    dest = db.query(models.Destination).filter(models.Destination.id == destination_id).first()
    if not dest:
        raise HTTPException(status_code=404, detail="Destino no encontrado")
    return dest

# response_model indica el schema para formatear la respuesta
# status_code indica el código HTTP a devolver al crear un recurso
@router.post("/", response_model=schemas.DestinationResponse, status_code=status.HTTP_201_CREATED)
def create_destination(destination: schemas.DestinationCreate, db: Session = Depends(get_db)):
    # Creo un nuevo objeto Destination a partir de los datos recibidos
    # destination.model_dump() convierte el schema Pydantic en un dict
    # ** descompone el dict en argumentos clave=valor para el constructor
    new_dest = Destination(**destination.model_dump())
    db.add(new_dest)
    db.commit()
    db.refresh(new_dest)
    # Devuelvo el nuevo destino creado
    return new_dest

# Endpoint para actualizar un destino existente
# response_model indica el schema para formatear la respuesta
@router.put("/{destination_id}", response_model=schemas.DestinationResponse)
# destination_id: ID del destino a actualizar
# updated_dest: datos actualizados del destino (schema DestinationCreate)
def update_destination(destination_id: int, updated_dest: schemas.DestinationCreate, db: Session = Depends(get_db)):
    print (destination_id)
    # Consulta para buscar el destino por ID
    dest_query = db.query(Destination).filter(Destination.id == destination_id)
    print (dest_query)
    # Obtengo el destino encontrado
    db_dest = dest_query.first()
    
    if not db_dest:
        raise HTTPException(status_code=404, detail="Destino no encontrado")
    
    # Actualizo los campos del destino con los nuevos datos
    # dest_query.update(...) actualiza los campos en la BD
    dest_query.update(updated_dest.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(db_dest)
    return db_dest

# response_model indica el schema para formatear la respuesta
@router.delete("/{destination_id}", status_code=status.HTTP_204_NO_CONTENT)
# Elimina un destino por su ID
# updated_dest: datos actualizados del destino (schema DestinationCreate) 
def delete_destination(destination_id: int, db: Session = Depends(get_db)):
    # Consulta para buscar el destino por ID
    db_dest = db.query(models.Destination).filter(models.Destination.id == destination_id).first()
    if not db_dest:
        raise HTTPException(status_code=404, detail="Destino no encontrado")
    
    db.delete(db_dest)
    db.commit()
    return None