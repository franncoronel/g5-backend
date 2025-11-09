import os
from pydantic import BaseModel
from typing import List, Optional, Tuple
import sqlite3


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
DB_PATH = os.path.join(BASE_DIR, "data", "recomendador.sqlite")

class PreferenciaDTO(BaseModel):
    generos: Optional[List[int]] = None
    rangoAnios: Tuple[int, int]
    duracion: Tuple[int, int]
    actores: Optional[List[str]] = None
    directores: Optional[List[str]] = None

class Preferencia():
    def __init__(
        self,
        generos: Optional[List[int]],
        rangoAnios: Tuple[int, int],
        duracion: Tuple[int, int],
        actores: Optional[List[str]],
        directores: Optional[List[str]]
    ):
        self.generos = generos
        self.rangoAnios = rangoAnios
        self.duracion = duracion
        self.actores = actores
        self.directores = directores

def conectarBase():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    return conn, cursor


def mapearPreferencia(preferenciaDTO:PreferenciaDTO):
    conn, cursor=conectarBase()
    try:
        generosMapeados = mapearGeneros(cursor,preferenciaDTO.generos)
        actoresMapeados = mapearPersonas(cursor,preferenciaDTO.actores)
        directoresMapeados=mapearPersonas(cursor,preferenciaDTO.directores)
        
        preferenciaMapeada = Preferencia(
            generos=generosMapeados,
            rangoAnios=preferenciaDTO.rangoAnios,
            duracion=preferenciaDTO.duracion,
            actores=actoresMapeados,
            directores=directoresMapeados
    )
        
        return preferenciaMapeada

    finally:
        conn.close()
    

def mapearGeneros(cursor, genre_ids: list[int]) -> list[int]:
    if not genre_ids:
        return []

    placeholders = ",".join(["?"] * len(genre_ids))
    cursor.execute(f"SELECT nombre FROM genero WHERE id IN ({placeholders})", genre_ids)
    result = cursor.fetchall()

    return [row[0] for row in result]
    

def mapearPersonas(cursor, person_ids: list[str]) -> list[str]:
    if not person_ids:
        return []

    placeholders = ",".join(["?"] * len(person_ids))
    cursor.execute(f"SELECT nombre FROM persona WHERE id IN ({placeholders})", person_ids)
    result = cursor.fetchall()

    return [row[0] for row in result]



#TODO:

#organizar codigo en diferentes archivos si es necesario

