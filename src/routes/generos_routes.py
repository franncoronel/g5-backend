from fastapi import APIRouter
from src.database.conexion import conectarBase


router = APIRouter()

@router.get("/generos")
def obtener_generos():
    conn, cursor=conectarBase()
    cursor.execute("SELECT id, nombre FROM genero")
    generos = [{"id": row[0], "nombre": row[1]} for row in cursor.fetchall()]
    conn.close()
    return generos