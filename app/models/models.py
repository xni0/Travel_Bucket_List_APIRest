from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

# Aqui le digo a Python como son las tablas de mi BD 
# Aqui es donde uso el ORM de SQLAlchemy para definir mis modelos
# La clase Base contiene logica para que SQLAlchemy pueda mapear estas clases a tablas físicas

class Destination(Base):  # Sirve como plantilla para la tabla 'destinations'
                          # Base es la clase magica de SQLAlchemy, cualquier clase que herede de 
                          # ella se convierte en una tabla en travel.db
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    country = Column(String)
    budget = Column(Float)
    visited = Column(Boolean, default=False)

    # Relación con actividades
    # Me permite acceder a las actividades de un destino sin hacer joins manuales
    # Como por ejemplo destination.activities en lugar de hacer una consulta separada
    activities = relationship("Activity", back_populates="destination", cascade="all, delete-orphan")

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    cost = Column(Float, default=0.0) 

    duration_minutes = Column(Integer, default=60) # Duración estimada
    category = Column(String, default="Turismo")   # Por ejemplo: Gastronomía, Aventura, Cultura
    requires_booking = Column(Boolean, default=False) # ¿Necesita reserva?
    
    # Foreign Key para vincular con destino
    destination_id = Column(Integer, ForeignKey("destinations.id"))

    # Relación inversa con destino
    destination = relationship("Destination", back_populates="activities")