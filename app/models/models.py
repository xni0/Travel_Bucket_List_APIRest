from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class Destination(Base):  # <--- Fíjate que es singular, "Destination"
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    country = Column(String)
    budget = Column(Float)
    visited = Column(Boolean, default=False)

    # Relación con actividades
    activities = relationship("Activity", back_populates="destination", cascade="all, delete-orphan")

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    cost = Column(Float, default=0.0) 
    
    destination_id = Column(Integer, ForeignKey("destinations.id"))

    destination = relationship("Destination", back_populates="activities")