from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models import models
from app.schemas import schemas

router = APIRouter(
    prefix="/destinations",
    tags=["Activities"]
)

# Crear actividad vinculada a un destino
@router.post("/{destination_id}/activities/", response_model=schemas.ActivityResponse)
def create_activity_for_destination(
    destination_id: int, 
    activity: schemas.ActivityCreate, 
    db: Session = Depends(get_db)
):
    # Primero comprobamos si el destino existe
    dest = db.query(models.Destination).filter(models.Destination.id == destination_id).first()
    if not dest:
        raise HTTPException(status_code=404, detail="Destino no encontrado")

    new_activity = models.Activity(**activity.model_dump(), destination_id=destination_id)
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    return new_activity