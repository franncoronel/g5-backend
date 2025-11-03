from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DB_PATH = "data/recomendador.sqlite"  
@app.get("/generos")
def obtener_generos():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre FROM genero")
    generos = [{"id": row[0], "nombre": row[1]} for row in cursor.fetchall()]
    conn.close()
    return generos