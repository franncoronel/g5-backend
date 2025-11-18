import sqlite3
from typing import Dict, Optional, List
from src.paths import DB_PATH


def obtener_titulo_por_id(id_titulo: str) -> Optional[Dict]:
    """
    Obtiene el detalle completo de un título por su ID, incluyendo:
    - Datos básicos del título
    - Géneros (array de strings)
    - Puntaje (rating)
    - Directores (array de strings)
    - Elenco (actores, array de strings)
    - Plataformas
    - Títulos alternativos (array de strings)
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. Datos básicos del título
    query_titulo = """
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
    cursor.execute(query_titulo, [id_titulo])
    resultado = cursor.fetchone()

    if not resultado:
        conn.close()
        return None

    titulo_data = dict(resultado)

    # 2. Géneros (solo nombres)
    query_generos = """
        SELECT g.nombre
        FROM genero g
        JOIN titulo_genero tg ON g.id = tg.id_genero
        WHERE tg.id_titulo = ?
    """
    cursor.execute(query_generos, [id_titulo])
    titulo_data["generos"] = [row["nombre"] for row in cursor.fetchall()]

    # 3. Puntaje
    query_puntaje = """
        SELECT promedio, cantidad_votos
        FROM puntaje
        WHERE id_titulo = ?
    """
    cursor.execute(query_puntaje, [id_titulo])
    puntaje_row = cursor.fetchone()
    titulo_data["puntaje"] = dict(puntaje_row) if puntaje_row else None

    # 4. Directores (solo nombres)
    query_directores = """
        SELECT p.nombre
        FROM persona p
        JOIN profesion_titulo pt ON p.id = pt.id_persona
        JOIN profesion pr ON pt.id_profesion = pr.id
        WHERE pt.id_titulo = ? AND LOWER(pr.nombre) = 'director'
    """
    cursor.execute(query_directores, [id_titulo])
    titulo_data["directores"] = [row["nombre"] for row in cursor.fetchall()]

    # 5. Elenco (solo nombres de actores)
    query_elenco = """
        SELECT p.nombre
        FROM persona p
        JOIN profesion_titulo pt ON p.id = pt.id_persona
        JOIN profesion pr ON pt.id_profesion = pr.id
        WHERE pt.id_titulo = ? AND LOWER(pr.nombre) = 'actor'
        LIMIT 10
    """
    cursor.execute(query_elenco, [id_titulo])
    titulo_data["elenco"] = [row["nombre"] for row in cursor.fetchall()]

    # 6. Plataformas (mantiene id y nombre)
    query_plataformas = """
        SELECT pl.id, pl.nombre
        FROM plataforma pl
        JOIN titulo_plataforma tp ON pl.id = tp.id_plataforma
        WHERE tp.id_titulo = ?
    """
    cursor.execute(query_plataformas, [id_titulo])
    titulo_data["plataformas"] = [dict(row) for row in cursor.fetchall()]

    # 7. Títulos alternativos (solo títulos)
    query_alternativos = """
        SELECT titulo
        FROM titulo_alternativo
        WHERE id_titulo = ?
        LIMIT 5
    """
    cursor.execute(query_alternativos, [id_titulo])
    titulo_data["titulos_alternativos"] = [row["titulo"] for row in cursor.fetchall()]

    conn.close()
    return titulo_data
