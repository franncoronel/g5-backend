import os
from pydantic import BaseModel
from typing import List, Optional, Tuple
import sqlite3

from src.database.entidades import Genero, Persona

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
DB_PATH = os.path.join(BASE_DIR, "data", "recomendador.sqlite")

class PreferenceDTO(BaseModel):
    genres: Optional[List[int]] = None
    yearRange: Tuple[int, int]
    duration: Tuple[int, int]
    actors: Optional[List[str]] = None
    directors: Optional[List[str]] = None


class Preference():
    genres: Optional[List[Genero]]
    #yearRange: Tuple[]
    duration: Tuple[int,int]
    actors: Optional[List[Persona]]
    directors: Optional[List[Persona]]

def mapPreference(preference:PreferenceDTO):
    conn, cursor=conectarBase()
    try:
        genres = mapGenres(cursor,preference.genres)
        actors = mapActors(cursor,preference.actors)
        directors=mapDirectors(cursor,preference.directors)
        
        mappedPreference = Preference(
            genres=genres,
            duration=preference.duration,
            actors=actors,
            directors=directors
    )

    finally:
        conn.close()
    
    return mappedPreference

def conectarBase():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    return conn, cursor

def mapGenres(cursor: sqlite3.Cursor, genresID: list[int]):
    genres = []
    for genre_id in genresID:
        cursor.execute("SELECT id, nombre FROM genero WHERE id = ?", (genre_id,))
        row = cursor.fetchone()
        if row:
            genres.append(Genero(id=row[0], nombre=row[1]))
    return genres
    

def mapActors(cursor: sqlite3.Cursor, actorsName: list[str]):
    actors = []
    for actorName in actorsName:
        cursor.execute("""
            SELECT * FROM persona
            WHERE LOWER(nombre) LIKE ?
        """, (f"%{actorName.lower()}%",))
        coincidencias = cursor.fetchall()
        actors.extend(coincidencias)
    return actors
    
    
def mapDirectors(cursor: sqlite3.Cursor,directorsName: list[str]):
    directors=[]
    for directorName in directorsName:
        cursor.execute("""
            SELECT * FROM persona
            WHERE LOWER(nombre) LIKE ?
        """, (f"%{directorName.lower()}%",))
        coincidencias = cursor.fetchall()
        directors.extend(coincidencias)
    return directors