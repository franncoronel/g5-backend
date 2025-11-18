from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class GeneroDTO(BaseModel):
    id: int
    nombre: str


class PuntajeDTO(BaseModel):
    promedio: float
    cantidad_votos: int


class PersonaDTO(BaseModel):
    id: str
    nombre: str
    nombre_personaje: Optional[str] = None


class PlataformaDTO(BaseModel):
    id: int
    nombre: str


class TituloAlternativoDTO(BaseModel):
    titulo: str
    es_original: bool
    region: Optional[str] = None
    idioma: Optional[str] = None


class TituloDetalleDTO(BaseModel):
    id: str
    tipo: str
    titulo: str
    duracion: int
    fecha_estreno: date
    idioma_original: Optional[str] = None
    sinopsis: Optional[str] = None
    poster: Optional[str] = None
    backdrop: Optional[str] = None
    generos: List[GeneroDTO] = []
    puntaje: Optional[PuntajeDTO] = None
    directores: List[PersonaDTO] = []
    elenco: List[PersonaDTO] = []
    plataformas: List[PlataformaDTO] = []
    titulos_alternativos: List[TituloAlternativoDTO] = []

    class Config:
        from_attributes = True
