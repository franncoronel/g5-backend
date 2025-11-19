from pydantic import BaseModel, Field
from typing import List, Optional, Tuple

from src.database.entidades import Genero, Persona

class PreferenciaDTO(BaseModel):
    genres: Optional[List[int]] = Field(None, alias="genres")
    yearRange: Tuple[int, int] = Field(..., alias="yearRange")
    duration: Tuple[int, int] = Field(..., alias="duration")
    actors: Optional[List[str]] = Field(None, alias="actors")
    directors: Optional[List[str]] = Field(None, alias="directors")

    class Config:
        populate_by_name = True

class Preferencia():
    def __init__(
        self,
        generos: Optional[List[Genero]],
        rangoAnios: Tuple[int, int],
        duracion: Tuple[int, int],
        actores: Optional[List[Persona]],
        directores: Optional[List[Persona]]
    ):
        self.generos = generos
        self.rangoAnios = rangoAnios
        self.duracion = duracion
        self.actores = actores
        self.directores = directores

