from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models import models
from app.schemas import schemas

# Definición del router para actividades
# Sirve para agrupar endpoints relacionados
router = APIRouter(
    prefix="/destinations",
    tags=["Activities"]
)

# Crear actividad vinculada a un destino
# la URL está anidada bajo /destinations/{destination_id}/activities/
# response_model indica el schema para formatear la respuesta
@router.post("/{destination_id}/activities/", response_model=schemas.ActivityResponse)
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