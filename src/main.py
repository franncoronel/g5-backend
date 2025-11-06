import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from src.models.preference import PreferenceDTO
'''
Correr con:
          python -m uvicorn src.main:app --reload
'''

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

#RECIBIR PREFERENCIA DEL FRONTEND
@app.post("/preferencias")
def recibir_preferencias(preferencia: PreferenceDTO):
    print("📩 Preferencias recibidas:")
    print(preferencia.model_dump())  # Versión en dict
    return {"mensaje": "Preferencias recibidas correctamente"}