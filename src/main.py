import os
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from typing import List, Dict

from src.models.preferencia import PreferenciaDTO

'''
Correr con:
          python -m uvicorn src.main:app --reload
'''

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # dirección del frontend
    allow_credentials=True,
    allow_methods=["*"],  # permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # permitir todos los headers
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
DB_PATH = os.path.join(BASE_DIR, "data", "recomendador.sqlite")

#GENEROS

@app.get("/generos")
def obtener_generos():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre FROM genero")
    generos = [{"id": row[0], "nombre": row[1]} for row in cursor.fetchall()]
    conn.close()
    return generos

@app.get("/actores")
def get_actores(busqueda: str = Query("", description="Texto para filtrar actores por nombre")):
    """
    Devuelve todas las personas que tengan la profesión 'actor' (id_profesion=1),
    opcionalmente filtradas por nombre.
    """
    return buscar_personas_por_profesion("1", busqueda)


@app.get("/directores")
def get_directores(busqueda: str = Query("", description="Texto para filtrar directores por nombre")):
    """
    Devuelve todas las personas que tengan la profesión 'director' (id_profesion=3),
    opcionalmente filtradas por nombre.
    """
    return buscar_personas_por_profesion("3", busqueda)

#RECIBIR PREFERENCIA DEL FRONTEND
@app.post("/preferencias")
def recibir_preferencias(preferencia: PreferenciaDTO):
    print("📩 Preferencias recibidas:")
    print(preferencia.model_dump())  # Versión en dict
    return {"mensaje": "Preferencias recibidas correctamente"}

def buscar_personas_por_profesion(id_profesion: str, busqueda: str = "") -> List[Dict]:
    """
    Busca personas que tengan la profesión indicada (id_profesion)
    y opcionalmente filtradas por nombre.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
        SELECT DISTINCT p.id, p.nombre
        FROM persona p
        JOIN profesion_titulo pt ON p.id = pt.id_persona
        WHERE pt.id_profesion = ?
    """

    params = [id_profesion]

    if busqueda:
        query += " AND p.nombre LIKE ?"
        params.append(f"%{busqueda}%")

    cursor.execute(query, params)
    resultados = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return resultados