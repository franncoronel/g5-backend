import sqlite3
from typing import Dict, List

from src.paths import DB_PATH


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
        params.append(f"{busqueda}%")

    cursor.execute(query, params)
    resultados = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return resultados