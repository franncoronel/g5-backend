# src/ai/embeddings.py
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from sentence_transformers import SentenceTransformer
import numpy as np

from src.database.entidades import (
    Titulo, TituloEmbedding, Titulo_Genero, Genero,
    Profesion_Titulo, Profesion, Persona
)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_embedder_singleton = None
def get_embedder():
    global _embedder_singleton
    if _embedder_singleton is None:
        _embedder_singleton = SentenceTransformer(MODEL_NAME)
    return _embedder_singleton

def _text_for_title(session: Session, t: Titulo) -> str:
    # Juntamos metadata útil para “describir” la película
    # géneros
    gens = session.execute(
        select(Genero.nombre)
        .join(Titulo_Genero, Genero.id == Titulo_Genero.id_genero)
        .where(Titulo_Genero.id_titulo == t.id)
    ).scalars().all()
    generos = ", ".join(gens) if gens else ""

    # profesiones (directores/actores principales)
    profs = session.execute(
        select(Profesion.nombre, Persona.nombre)
        .join(Profesion_Titulo, Profesion.id == Profesion_Titulo.id_profesion)
        .join(Persona, Persona.id == Profesion_Titulo.id_persona)
        .where(Profesion_Titulo.id_titulo == t.id)
    ).all()

    directores = [p[1] for p in profs if p[0].lower() == "director"]
    actores = [p[1] for p in profs if p[0].lower() == "actor"]

    # texto base
    partes = [
        f"title: {t.titulo}",
        f"type: {t.tipo.name.lower()}",
        f"year: {t.fecha_estreno.year}",
        f"duration_min: {t.duracion}",
    ]
    if generos: partes.append(f"genres: {generos}")
    if directores: partes.append(f"directors: {', '.join(directores[:5])}")
    if actores: partes.append(f"actors: {', '.join(actores[:5])}")
    if t.sinopsis: partes.append(f"plot: {t.sinopsis}")

    return " | ".join(partes)

def ensure_title_embeddings(session: Session, batch_size: int = 10000) -> int:
    """
    Crea embeddings solo para títulos que no tienen embedding almacenado.
    Hace commits parciales cada `batch_size` registros.
    Devuelve la cantidad creada.
    """
    embedder = get_embedder()
    # Títulos sin embedding
    missing = session.execute(
        select(Titulo)
        .outerjoin(TituloEmbedding, TituloEmbedding.id_titulo == Titulo.id)
        .where(TituloEmbedding.id_titulo.is_(None))
    ).scalars().all()

    if not missing:
        return 0

    total_created = 0

    # Procesar en lotes
    for i in range(0, len(missing), batch_size):
        batch = missing[i:i + batch_size]

        texts: List[str] = [_text_for_title(session, t) for t in batch]
        mat = embedder.encode(texts, normalize_embeddings=True)
        dim = mat.shape[1]

        for t, vec in zip(batch, mat):
            session.merge(TituloEmbedding(
                id_titulo=t.id,
                model=MODEL_NAME,
                dim=int(dim),
                vector=vec.astype(float).tolist()
            ))

        # ✅ Commit parcial cada batch
        session.commit()
        total_created += len(batch)
        print(f"  ✓ Embeddings guardados: {total_created}/{len(missing)} ({(total_created/len(missing)*100):.1f}%)")

    return total_created

def embed_query_from_preference(pref) -> np.ndarray:
    """
    pref: instancia de PreferenciaDTO (o dict) ya validada.
    La convertimos a un texto estilo 'consulta' y la embebemos.
    """
    # Armamos un texto descriptivo con soft constraints (no filtra duro)
    genres = ", ".join(pref.genres) if getattr(pref, "genres", None) else ""
    yr = getattr(pref, "yearRange", None) or []
    dur = getattr(pref, "duration", None) or []
    actors = getattr(pref, "actors", "") or ""
    directors = getattr(pref, "directors", "") or ""

    parts = ["Find movies"]
    if genres: parts.append(f"in genres: {genres}")
    if yr: parts.append(f"released between: {yr[0]} and {yr[1]}")
    if dur: parts.append(f"duration between: {dur[0]} and {dur[1]} minutes")
    if actors: parts.append(f"related to actors: {actors}")
    if directors: parts.append(f"or directors: {directors}")

    query_text = " | ".join(parts)
    emb = get_embedder().encode([query_text], normalize_embeddings=True)
    return emb[0]  # (dim,)
