from pydantic import BaseModel, Field
from typing import List, Optional, Tuple

class PreferenciaDTO(BaseModel):
    generos: Optional[List[int]] = Field(None, alias="genres")
    rangoAnios: Tuple[int, int] = Field(..., alias="yearRange")
    duracion: Tuple[int, int] = Field(..., alias="duration")
    actores: Optional[List[str]] = Field(None, alias="actors")
    directores: Optional[List[str]] = Field(None, alias="directors")

    class Config:
        populate_by_name = True

class Preferencia():
    def __init__(
        self,
        generos: Optional[List[int]],
        rangoAnios: Tuple[int, int],
        duracion: Tuple[int, int],
        actores: Optional[List[str]],
        directores: Optional[List[str]]
    ):
        self.generos = generos
        self.rangoAnios = rangoAnios
        self.duracion = duracion
        self.actores = actores
        self.directores = directores

