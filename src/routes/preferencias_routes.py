from fastapi import APIRouter, Query
import numpy as np
from src.mappers import mapearPreferencia
from src.models.preferencia import PreferenciaDTO
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

@router.post("/preferencias")
def recibir_preferencias(
        preferenciaDTO: PreferenciaDTO,
        top_k: int = Query(20, ge=1, le=200),
        alpha: float = Query(0.8, ge=0.0, le=1.0)
    ):
    """
    Retorna las mejores películas según similitud de embeddings con la preferencia.
    Mezcla (opcional) con rating usando: score = alpha * sim + (1-alpha) * rating_norm
    - top_k: cantidad de resultados
    - alpha: peso de la similitud (1.0 = solo embedding)
    """

    q_vec = embed_query_from_preference(preferenciaDTO)  # np.array (dim,)

    with Session(motor) as s:
        rows = s.execute(
            select(Titulo, TituloEmbedding, Puntaje)
            .join(TituloEmbedding, Titulo.id == TituloEmbedding.id_titulo)
            .outerjoin(Puntaje, Puntaje.id_titulo == Titulo.id)
        ).all()

        if not rows:
            return {"items": [], "count": 0}

        # Matriz de embeddings [n, dim] y metadata
        vecs = []
        metas = []
        for t, emb, punt in rows:
            vecs.append(np.array(emb.vector, dtype=np.float32))
            metas.append((t, punt))
        M = np.vstack(vecs)  # [n, dim]
        # similitud coseno asumiendo embeddings normalizados
        sims = (M @ q_vec).astype(float)  # [n,] porque ambos normalizados

        # Score mixto con rating (opcional)
        scores = []
        for i, (t, punt) in enumerate(metas):
            r = _normalize_rating(getattr(punt, "promedio", None))
            score = alpha * float(sims[i]) + (1.0 - alpha) * r
            scores.append((score, i))

        scores.sort(key=lambda x: x[0], reverse=True)
        top = scores[:top_k]

        items = []
        for score, idx in top:
            t, punt = metas[idx]
            items.append({
                "id": t.id,
                "title": t.titulo,
                "year": t.fecha_estreno.year,
                "duration": t.duracion,
                "poster": t.poster,
                "rating": getattr(punt, "promedio", None),
                "similarity": float(sims[idx]),
                "score": float(score)
            })

        return {"items": items, "count": len(items)}