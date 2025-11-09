import os
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from typing import List, Dict
from src.models.preference import PreferenceDTO, conectarBase
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

@app.get("/personas")
def buscar_personas(rol: str = None, nombre: str = ""):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Primero verificamos si existe la columna 'rol'
        cursor.execute("PRAGMA table_info(persona)")
        columnas = [col[1] for col in cursor.fetchall()]

        if "rol" in columnas and rol:
            # Si la columna 'rol' existe, filtramos por rol y nombre
            cursor.execute("""
                SELECT * FROM persona
                WHERE rol = ? AND nombre LIKE ?
            """, (rol, f"%{nombre}%"))
        else:
            # Si no existe 'rol', solo filtramos por nombre
            cursor.execute("""
                SELECT * FROM persona
                WHERE nombre LIKE ?
            """, (f"%{nombre}%",))

        resultados = cursor.fetchall()
        conn.close()

        # Convertimos los resultados en objetos legibles
        return [
            {"id": r[0], "nombre": r[1]} for r in resultados
        ]

    except Exception as e:
        conn.close()
        return {"error": str(e)}

#RECIBIR PREFERENCIA DEL FRONTEND
@app.post("/preferencias")
def recibir_preferencias(preferencia: PreferenceDTO):
    print("📩 Preferencias recibidas:")
    print(preferencia.model_dump())  # Versión en dict
    return {"mensaje": "Preferencias recibidas correctamente"}
