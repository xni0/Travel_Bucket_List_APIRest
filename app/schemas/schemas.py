from pydantic import BaseModel, ConfigDict
from typing import List, Optional

# Aqui se realiza la validación de datos - Pydantic - para las actividades
# SCHEMAS PARA ACTIVIDADES

# Creo 3 clases porque uso diferentes datos en cada caso:
# - ActivityBase: datos comunes a todas las operaciones
# - ActivityCreate: datos necesarios para crear una actividad
# - ActivityResponse: datos que devuelvo al cliente al consultar actividades
class ActivityBase(BaseModel):
    name: str
    cost: float = 0.0
    duration_minutes: int = 60
    category: str = "Turismo"
    requires_booking: bool = False

class ActivityCreate(ActivityBase):
    pass

# Esquema para actualizaciones parciales
class ActivityUpdate(BaseModel):
    name: Optional[str] = None
    cost: Optional[float] = None
    duration_minutes: Optional[int] = None
    category: Optional[str] = None
    requires_booking: Optional[bool] = None

class ActivityResponse(ActivityBase):
    id: int
    destination_id: int

    model_config = ConfigDict(from_attributes=True)

# SCHEMAS PARA DESTINOS 
class DestinationBase(BaseModel):
    name: str
    country: str
    budget: float
    visited: bool = False

class DestinationCreate(DestinationBase):
    pass

class DestinationResponse(DestinationBase):
    id: int
    # La magia: devolvemos la lista de actividades dentro del destino´
    # Permite que al consultar un destino, también obtengamos sus actividades
    activities: List[ActivityResponse] = []

    model_config = ConfigDict(from_attributes=True)