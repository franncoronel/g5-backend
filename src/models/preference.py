from pydantic import BaseModel
from typing import List, Optional, Tuple

class PreferenceDTO(BaseModel):
    genres: Optional[List[int]] = None
    yearRange: Tuple[int, int]
    duration: Tuple[int, int]
    actors: Optional[List[int]] = None
    directors: Optional[List[int]] = None