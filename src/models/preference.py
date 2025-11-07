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
        duration: Tuple[int, int],
        actors: Optional[List[str]],
        directors: Optional[List[str]]
    ):
        self.genres = genres
        self.duration = duration
        self.actors = actors
        self.directors = directors

def mapPreference(preferenceDTO:PreferenceDTO):
    conn, cursor=conectarBase()
    try:
        mappedGenres = mapGenres(cursor,preferenceDTO.genres)
        mappedActors = mapActors(cursor,preferenceDTO.actors)
        mappedDirectors=mapDirectors(cursor,preferenceDTO.directors)
        
        mappedPreference = Preference(
            genres=mappedGenres,
            duration=preferenceDTO.duration,
            actors=mappedActors,
            directors=mappedDirectors
    )
        
        return mappedPreference

    finally:
        conn.close()
    
    

def conectarBase():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    return conn, cursor

def mapGenres(cursor, genre_ids: list[int]) -> list[int]:
    if not genre_ids:
        return []

    placeholders = ",".join(["?"] * len(genre_ids))
    cursor.execute(f"SELECT id FROM genero WHERE id IN ({placeholders})", genre_ids)
    result = cursor.fetchall()

    return [row[0] for row in result]
    

def mapActors(cursor, actors_ids: list[str]) -> list[str]:
    if not actors_ids:
        return []

    # Verificamos que existan en la tabla persona
    placeholders = ",".join(["?"] * len(actors_ids))
    cursor.execute(f"SELECT id FROM persona WHERE id IN ({placeholders})", actors_ids)
    result = cursor.fetchall()

    # Retornamos solo los IDs existentes
    return [row[0] for row in result]


def mapDirectors(cursor, directors_ids: list[str]) -> list[str]:
    if not directors_ids:
        return []

    placeholders = ",".join(["?"] * len(directors_ids))
    cursor.execute(f"SELECT id FROM persona WHERE id IN ({placeholders})", directors_ids)
    result = cursor.fetchall()

    return [row[0] for row in result]

#TODO:

#chequear que las personas existan como directores/actores en nuestra tabla y que si no se ignoren, como esta ahora podria
#pasar que mappee a alguien porque figura en la tabla pero solo lo conozca como director

#una vez hecho eso generalizar mapPersonas

#chequear antes de mapear si el dto tiene esos datos (genero, actores, directores)

#agregar yearRange

#organizar codigo en diferentes archivos si es necesario
