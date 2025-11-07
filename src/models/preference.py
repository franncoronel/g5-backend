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
    conn, cursor=conectarBase
    try:
        genres = mapGenres(cursor,preference.genres)

    finally:
        conn.close()
    


def conectarBase():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    return conn, cursor

def mapGenres(cursor:sqlite3.Cursor,genresID:List[int]):
    genres = []
    for genreID in genresID:
        cursor.execute("SELECT * FROM genero",(genreID))
        genero=cursor.fetchone()
        if genero:
            genres.append(genero)
    
    return genres
    

# def mapActors(cursor:sqlite3.cursor,actorsName:List[str]):
#     actors = []
#     for actorName in actorsName:
#         cursor.execute("SELECT * FROM profesion_titulo")
    
    
