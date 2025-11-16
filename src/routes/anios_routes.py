from fastapi import APIRouter
from src.database.conexion import conectarBase

router = APIRouter()

@router.get("/anios")
def obtener_rango_anios():
    conn, cursor = conectarBase()

    cursor.execute("""
        SELECT 
            MIN(substr(fecha_estreno, 1, 4)),
            MAX(substr(fecha_estreno, 1, 4))
        FROM titulo
    """)
    
    resultado = cursor.fetchone()
    conn.close()

    min_year, max_year = resultado

    return {
        "min_year": int(min_year) if min_year else None,
        "max_year": int(max_year) if max_year else None
    }