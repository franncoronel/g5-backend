from src.database.setup import Base
from datetime import date
from enum import Enum
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

class TipoTitulo(Enum):
    PELICULA = "pelicula"

class Titulo(Base):
    __tablename__ = "titulo"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[TipoTitulo]
    titulo: Mapped[str]
    duracion: Mapped[int]

class Pelicula(Titulo):
    __tablename__ = "pelicula"
    
    id: Mapped[int]
    fechaEstreno: Mapped[date] 

class Genero(Base):
    __tablename__ = "genero"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    
class Puntaje(Base):
    __tablename__ = "puntaje"
    
    promedio: Mapped[float]
    votos: Mapped[int]