from fastapi import APIRouter
from src.database.conexion import conectarBase
from src.utils.traduccion import traducir_genero


router = APIRouter()

@router.get("/generos")
def obtener_generos():
    conn, cursor=conectarBase()
    cursor.execute("SELECT id, nombre FROM genero")
    generos = cursor.fetchall()
    conn.close()

    generos_traducidos = [
        {"id": row[0], "nombre": traducir_genero(row[1])}
        for row in generos
    ]

    return generos_traducidos