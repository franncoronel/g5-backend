from src.database.conexion import conectarBase
from src.models.preferencia import Preferencia, PreferenciaDTO


def mapearPreferencia(preferenciaDTO:PreferenciaDTO):
    conn, cursor=conectarBase()
    try:
        generosMapeados = mapearGeneros(cursor,preferenciaDTO.generos)
        actoresMapeados = mapearPersonas(cursor,preferenciaDTO.actores)
        directoresMapeados=mapearPersonas(cursor,preferenciaDTO.directores)
        
        preferenciaMapeada = Preferencia(
            generos=generosMapeados,
            rangoAnios=preferenciaDTO.rangoAnios,
            duracion=preferenciaDTO.duracion,
            actores=actoresMapeados,
            directores=directoresMapeados
    )
        
        return preferenciaMapeada

    finally:
        conn.close()
    

def mapearGeneros(cursor, genre_ids: list[int]) -> list[int]:
    if not genre_ids:
        return []

    placeholders = ",".join(["?"] * len(genre_ids))
    cursor.execute(f"SELECT nombre FROM genero WHERE id IN ({placeholders})", genre_ids)
    result = cursor.fetchall()

    return [row[0] for row in result]
    

def mapearPersonas(cursor, person_ids: list[str]) -> list[str]:
    if not person_ids:
        return []

    placeholders = ",".join(["?"] * len(person_ids))
    cursor.execute(f"SELECT nombre FROM persona WHERE id IN ({placeholders})", person_ids)
    result = cursor.fetchall()

    return [row[0] for row in result]
