from pydantic import BaseModel, ConfigDict
from typing import List, Optional

# --- SCHEMAS PARA ACTIVIDADES ---
class ActivityBase(BaseModel):
    name: str
    cost: float = 0.0

class ActivityCreate(ActivityBase):
    pass

class ActivityResponse(ActivityBase):
    id: int
    destination_id: int

    model_config = ConfigDict(from_attributes=True) 

# --- SCHEMAS PARA DESTINOS ---
class DestinationBase(BaseModel):
    name: str
    country: str
    budget: float
    visited: bool = False

class DestinationCreate(DestinationBase):
    pass

class DestinationResponse(DestinationBase):
    id: int
    # La magia: devolvemos la lista de actividades dentro del destino
    activities: List[ActivityResponse] = []

    model_config = ConfigDict(from_attributes=True)