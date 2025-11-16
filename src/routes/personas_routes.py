from fastapi import APIRouter, Query
from src.repositories.personas_repository import buscar_personas_por_profesion

router = APIRouter()

@router.get("/actores")
def get_actores(busqueda: str = Query("", description="Texto para filtrar actores por nombre")):
    """
    Devuelve todas las personas que tengan la profesión 'actor' (id_profesion=1),
    opcionalmente filtradas por nombre.
    """
    return buscar_personas_por_profesion("1", busqueda)


@router.get("/directores")
def get_directores(busqueda: str = Query("", description="Texto para filtrar directores por nombre")):
    """
    Devuelve todas las personas que tengan la profesión 'director' (id_profesion=3),
    opcionalmente filtradas por nombre.
    """
    return buscar_personas_por_profesion("3", busqueda)