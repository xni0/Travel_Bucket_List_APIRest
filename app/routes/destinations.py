from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.models import models
from app.schemas import schemas

router = APIRouter(
    prefix="/destinations",
    tags=["Destinations"]
)

@router.get("/", response_model=List[schemas.DestinationResponse])
def get_destinations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Destination).offset(skip).limit(limit).all()

@router.get("/{destination_id}", response_model=schemas.DestinationResponse)
def get_destination(destination_id: int, db: Session = Depends(get_db)):
    dest = db.query(models.Destination).filter(models.Destination.id == destination_id).first()
    if not dest:
        raise HTTPException(status_code=404, detail="Destino no encontrado")
    return dest

@router.post("/", response_model=schemas.DestinationResponse, status_code=status.HTTP_201_CREATED)
def create_destination(destination: schemas.DestinationCreate, db: Session = Depends(get_db)):
    new_dest = models.Destination(**destination.model_dump())
    db.add(new_dest)
    db.commit()
    db.refresh(new_dest)
    return new_dest

@router.put("/{destination_id}", response_model=schemas.DestinationResponse)
def update_destination(destination_id: int, updated_dest: schemas.DestinationCreate, db: Session = Depends(get_db)):
    dest_query = db.query(models.Destination).filter(models.Destination.id == destination_id)
    db_dest = dest_query.first()
    
    if not db_dest:
        raise HTTPException(status_code=404, detail="Destino no encontrado")
    
    dest_query.update(updated_dest.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(db_dest)
    return db_dest

@router.delete("/{destination_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_destination(destination_id: int, db: Session = Depends(get_db)):
    db_dest = db.query(models.Destination).filter(models.Destination.id == destination_id).first()
    if not db_dest:
        raise HTTPException(status_code=404, detail="Destino no encontrado")
    
    db.delete(db_dest)
    db.commit()
    return None