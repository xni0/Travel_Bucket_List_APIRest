from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models import models
from app.schemas import schemas
from typing import List

# Definición del router para actividades
# Sirve para agrupar endpoints relacionados
router = APIRouter(
    prefix="/destinations",
    tags=["Activities"]
)


# Crear actividad vinculada a un destino
# la URL está anidada bajo /destinations/{destination_id}/activities/
# response_model indica el schema para formatear la respuesta
@router.post("/{destination_id}/activities/", response_model=schemas.ActivityResponse, status_code=status.HTTP_201_CREATED)
def create_activity_for_destination(
    destination_id: int, 
    # El cuerpo de la petición debe cumplir con el schema ActivityCreate
    activity: schemas.ActivityCreate, 
    # Inyección de dependencia para obtener la sesión de BD
    db: Session = Depends(get_db)
):
    # Primero comprobamos si el destino existe con esta consulta
    # Que en sql sería SELECT * FROM destinations WHERE id = [destination_id] LIMIT 1;
    # Si no existe, devolvemos un error 404
    dest = db.query(models.Destination).filter(models.Destination.id == destination_id).first()
    if not dest:
        raise HTTPException(status_code=404, detail="Destino no encontrado")

    # Si el destino existe, creamos la nueva actividad vinculada a ese destino
    # activity.model_dump() convierte el schema Pydantic en un dict
    # ** descompone el dict en argumentos clave=valor para el constructor
    new_activity = models.Activity(**activity.model_dump(), destination_id=destination_id)
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    return new_activity


# Obtener todas las actividades de un destino específico
@router.get("/{destination_id}/activities/", response_model=List[schemas.ActivityResponse])
def read_activities(destination_id: int, db: Session = Depends(get_db)):
    # Verificamos primero el destino
    dest = db.query(models.Destination).filter(models.Destination.id == destination_id).first()
    if not dest:
        raise HTTPException(status_code=404, detail="Destino no encontrado")
    
    # Retornamos la lista de actividades asociadas
    return db.query(models.Activity).filter(models.Activity.destination_id == destination_id).all()

# Obtener una actividad específica por su ID
@router.get("/activities/{activity_id}", response_model=schemas.ActivityResponse)
def read_activity(activity_id: int, db: Session = Depends(get_db)):
    # Buscamos la actividad directamente por su ID único
    activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    return activity


# Actualizar una actividad existente
@router.put("/activities/{activity_id}", response_model=schemas.ActivityResponse)
def update_activity(
    activity_id: int, 
    activity_update: schemas.ActivityUpdate, 
    db: Session = Depends(get_db)
):
    # Buscamos la actividad en la base de datos
    db_activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if not db_activity:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")

    # Convertimos los datos de entrada en un diccionario, excluyendo valores no enviados (unset)
    update_data = activity_update.model_dump(exclude_unset=True)
    
    # Iteramos sobre el diccionario para actualizar los atributos del modelo
    for key, value in update_data.items():
        setattr(db_activity, key, value)

    db.commit()
    db.refresh(db_activity)
    return db_activity


# Eliminar una actividad
@router.delete("/activities/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    # Buscamos el registro
    activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    
    # Eliminamos y confirmamos los cambios
    db.delete(activity)
    db.commit()
    # Al usar 204 No Content, no se devuelve cuerpo en la respuesta
    return None