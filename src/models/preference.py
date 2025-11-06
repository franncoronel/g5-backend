from pydantic import BaseModel
from typing import List, Optional, Tuple

from src.database.entidades import Genero, Persona


class PreferenceDTO(BaseModel):
    genres: Optional[List[int]] = None
    yearRange: Tuple[int, int]
    duration: Tuple[int, int]
    actors: Optional[List[str]] = None
    directors: Optional[List[str]] = None

#    def createPreference():

class Preference():
    genres: Optional[List[Genero]]
    #yearRange: Tuple[]
    duration: Tuple[int,int]
    actors: Optional[List[Persona]]
    directors: Optional[List[Persona]]