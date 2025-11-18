import sqlite3
from typing import Dict, Optional

from src.paths import DB_PATH


def obtener_titulo_por_id(id_titulo: str) -> Optional[Dict]:
    """
    Obtiene el detalle completo de un título por su ID.
    Retorna un diccionario con todos los campos o None si no existe.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
        SELECT
            id,
            tipo,
            titulo,
            duracion,
            fecha_estreno,
            idioma_original,
            sinopsis,
            poster,
            backdrop
        FROM titulo
        WHERE id = ?
    """

    cursor.execute(query, [id_titulo])
    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        return dict(resultado)
    return None
