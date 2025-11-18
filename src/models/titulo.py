from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class PuntajeDTO(BaseModel):
    promedio: float
    cantidad_votos: int


class PlataformaDTO(BaseModel):
    id: int
    nombre: str


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
    generos: List[str] = []
    puntaje: Optional[PuntajeDTO] = None
    directores: List[str] = []
    elenco: List[str] = []
    plataformas: List[PlataformaDTO] = []
    titulos_alternativos: List[str] = []

    class Config:
        from_attributes = True
