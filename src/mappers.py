from typing import List
from src.database.conexion import conectarBase
from src.database.entidades import Genero, Persona
from src.models.preferencia import Preferencia, PreferenciaDTO


def mapearPreferencia(preferenciaDTO:PreferenciaDTO):
    conn, cursor=conectarBase()
    print("En mapear")
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


def mapearGeneros(cursor, genre_ids: List[int]) -> List[Genero]:
    if not genre_ids:
        return []

    placeholders = ",".join(["?"] * len(genre_ids))
    cursor.execute(f"SELECT * FROM genero WHERE id IN ({placeholders})", genre_ids)
    result = cursor.fetchall()
    return result


def mapearPersonas(cursor, person_ids: List[str]) -> List[Persona]:
    if not person_ids:
        return []

    placeholders = ",".join(["?"] * len(person_ids))
    cursor.execute(f"SELECT * FROM persona WHERE id IN ({placeholders})", person_ids)
    result = cursor.fetchall()
    return result
