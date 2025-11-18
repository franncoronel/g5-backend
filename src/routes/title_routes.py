from fastapi import APIRouter, Query, HTTPException
import numpy as np
from src.mappers import mapearPreferencia
from src.models.preferencia import PreferenciaDTO
from src.models.titulo import TituloDetalleDTO
from src.repositories.titulos_repository import obtener_titulo_por_id
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.ai.embeddings import embed_query_from_preference
from src.database.entidades import motor, Titulo, TituloEmbedding, Puntaje


router = APIRouter()

def _normalize_rating(r: float | None) -> float:
    if r is None:
        return 0.0
    # IMDB-like (0..10) -> (0..1)
    return max(0.0, min(1.0, r / 10.0))

@router.get("/pelicula/{peliculaId}", response_model=TituloDetalleDTO)
def devolver_detalle_pelicula(peliculaId: str):
    """
    Retorna el detalle de la película según el ID de la misma
    """
    print(f"Buscando detalle de película con ID: {peliculaId}")
    titulo = obtener_titulo_por_id(peliculaId)

    if not titulo:
        raise HTTPException(status_code=404, detail="Película no encontrada")

    return TituloDetalleDTO(**titulo)
