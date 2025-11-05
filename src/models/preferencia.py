from pydantic import BaseModel
from typing import List, Tuple

class Preferencia(BaseModel):
    genres: List[str]
    yearRange: Tuple[int, int]
    duration: Tuple[int, int]
    actors: List[str]
    directors: List[str]