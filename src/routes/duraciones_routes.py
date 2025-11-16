from fastapi import APIRouter
from src.database.conexion import conectarBase

router = APIRouter()

@router.get("/duraciones")
def obtener_rango_duracion():
    conn, cursor = conectarBase()

    cursor.execute("""
        SELECT 
            MIN(duracion),
            MAX(duracion)
        FROM titulo
    """)
    
    resultado = cursor.fetchone()
    conn.close()

    min_duracion, max_duracion = resultado

    return {
        "min_duracion": int(min_duracion) if min_duracion is not None else None,
        "max_duracion": int(max_duracion) if max_duracion is not None else None
    }
