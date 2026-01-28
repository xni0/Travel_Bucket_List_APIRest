from pydantic import BaseModel, ConfigDict
from typing import List, Optional

# Aqui se realiza la validación de datos para las actividades
# SCHEMAS PARA ACTIVIDADES

# Creo 3 clases porque uso diferentes datos en cada caso:
# - ActivityBase: datos comunes a todas las operaciones
# - ActivityCreate: datos necesarios para crear una actividad
# - ActivityResponse: datos que devuelvo al cliente al consultar actividades
class ActivityBase(BaseModel):
    name: str
    cost: float = 0.0

# Copia de ActivityBase, ya que para crear una actividad
# no necesito datos adicionales
# Es como el ticket de entrada (Lo que envia el usuario)
class ActivityCreate(ActivityBase):
    pass

# Respuesta al crear o consultar una actividad
# Es como el ticket de salida (Lo que recibe el usuario)
class ActivityResponse(ActivityBase):
    id: int
    destination_id: int

    # La magia: permite crear el objeto desde un modelo ORM
    # Ya que SQLAlchemy devuelve objetos de sus modelos
    # y Pydantic por defecto no sabe cómo manejarlos (Solo dicts/JSON)
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