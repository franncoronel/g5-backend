from src.database.setup import Base
from datetime import date
from enum import Enum
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

class Persona(Base):
    __tablename__ = "persona"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    
class Director(Persona):
    __tablename__ = "director"
    
class Actor(Persona):
    __tablename__ = "actor"
    
    rol: Mapped[str]