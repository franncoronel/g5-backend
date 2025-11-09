import os
from pydantic import BaseModel
from typing import List, Optional, Tuple
import sqlite3


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
DB_PATH = os.path.join(BASE_DIR, "data", "recomendador.sqlite")

class PreferenceDTO(BaseModel):
    genres: Optional[List[int]] = None
    yearRange: Tuple[int, int]
    duration: Tuple[int, int]
    actors: Optional[List[str]] = None
    directors: Optional[List[str]] = None

#@dataclass
class Preference():
    def __init__(
        self,
        genres: Optional[List[int]],
        yearRange: Tuple[int, int],
        duration: Tuple[int, int],
        actors: Optional[List[str]],
        directors: Optional[List[str]]
    ):
        self.genres = genres
        self.yearRange = yearRange
        self.duration = duration
        self.actors = actors
        self.directors = directors

def conectarBase():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    return conn, cursor


def mapPreference(preferenceDTO:PreferenceDTO):
    conn, cursor=conectarBase()
    try:
        mappedGenres = mapGenres(cursor,preferenceDTO.genres)
        mappedActors = mapPerson(cursor,preferenceDTO.actors)
        mappedDirectors=mapPerson(cursor,preferenceDTO.directors)
        
        mappedPreference = Preference(
            genres=mappedGenres,
            duration=preferenceDTO.duration,
            actors=mappedActors,
            directors=mappedDirectors
    )
        
        return mappedPreference

    finally:
        conn.close()
    

def mapGenres(cursor, genre_ids: list[int]) -> list[int]:
    if not genre_ids:
        return []

    placeholders = ",".join(["?"] * len(genre_ids))
    cursor.execute(f"SELECT nombre FROM genero WHERE id IN ({placeholders})", genre_ids)
    result = cursor.fetchall()

    return [row[0] for row in result]
    

def mapPerson(cursor, person_ids: list[str]) -> list[str]:
    if not person_ids:
        return []

    placeholders = ",".join(["?"] * len(person_ids))
    cursor.execute(f"SELECT nombre FROM persona WHERE id IN ({placeholders})", person_ids)
    result = cursor.fetchall()

    return [row[0] for row in result]



#TODO:


#una vez hecho eso generalizar mapPersonas

#organizar codigo en diferentes archivos si es necesario

#traducir para consistencia en idioma

#traducir generos o matarme
