from pydantic import BaseModel
from datetime import date
from typing import Optional


class TituloDetalleDTO(BaseModel):
    id: str
    tipo: str
    titulo: str
    duracion: int
    fecha_estreno: date
    idioma_original: Optional[str]
    sinopsis: Optional[str]
    poster: Optional[str]
    backdrop: Optional[str]

    class Config:
        from_attributes = True
