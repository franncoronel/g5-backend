# src/services/search_service.py
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter # ✅ Necesitamos esto para contar coincidencias

from src.database.entidades import Titulo, TituloEmbedding, Puntaje, Titulo_Genero
from src.ai.embeddings import embed_query_from_preference

def obtener_recomendaciones_hibridas(pref, session: Session, top_k: int = 10):
    """
    Estrategia Mejorada:
    1. Filtra por SQL (Año, Duración, Géneros).
    2. Si una película coincide con MÁS DE UN GÉNERO seleccionado, recibe un BONUS.
    3. Ordena por IA + Bonus.
    """
    print(f"🚀 Iniciando búsqueda inteligente para: {pref.genres}")

    query_vector = embed_query_from_preference(pref, session)
    
    # --- PASO 1: Filtros SQL ---
    filtros = []
    
    if getattr(pref, "yearRange", None) and len(pref.yearRange) == 2:
        filtros.append(Titulo.fecha_estreno >= f"{pref.yearRange[0]}-01-01")
        filtros.append(Titulo.fecha_estreno <= f"{pref.yearRange[1]}-12-31")

    if getattr(pref, "duration", None) and len(pref.duration) == 2:
        filtros.append(Titulo.duracion.between(pref.duration[0], pref.duration[1]))

    # Filtro de Géneros
    join_generos = False
    if getattr(pref, "genres", None) and len(pref.genres) > 0:
        filtros.append(Titulo_Genero.id_genero.in_(pref.genres))
        join_generos = True

    # --- PASO 2: Query (Trae duplicados intencionalmente) ---
    stmt = (
        select(Titulo, TituloEmbedding, Puntaje)
        .join(TituloEmbedding, Titulo.id == TituloEmbedding.id_titulo)
        .outerjoin(Puntaje, Titulo.id == Puntaje.id_titulo)
    )
    
    if join_generos:
        stmt = stmt.join(Titulo_Genero, Titulo.id == Titulo_Genero.id_titulo)
    
    if filtros:
        stmt = stmt.where(and_(*filtros))
    
    stmt = stmt.limit(3000) # Traemos más para poder filtrar bien

    resultados_raw = session.execute(stmt).all() 
    
    if not resultados_raw:
        return []

    # --- PASO 3: Detección de peliculas que matcheen bien a + de 1 genero ---
    # Si pedis [Terror, Comedia], la query SQL traerá 2 veces la misma película 
    # si esa película tiene AMBOS géneros.
    
    ids_peliculas = [r[0].id for r in resultados_raw]
    conteo_coincidencias = Counter(ids_peliculas) # Ej: {'tt123': 2, 'tt456': 1}

    # --- PASO 4: Calcular IA ---
    candidatos_vectores = np.array([r[1].vector for r in resultados_raw])
    query_vec_reshaped = query_vector.reshape(1, -1)
    scores_ia = cosine_similarity(query_vec_reshaped, candidatos_vectores)[0]

    # --- PASO 5: Ranking con BONUS ---
    ranking = []
    seen_ids = set()

    for idx, score in enumerate(scores_ia):
        titulo_obj = resultados_raw[idx][0]
        puntaje_obj = resultados_raw[idx][2]
        peli_id = titulo_obj.id
        
        if peli_id not in seen_ids:
            # 💡 LÓGICA DEL BONUS:
            # Cuantos más géneros coincidan, más multiplicamos el score.
            # Coincidencias: 1 -> Multiplicador 1.0 (Normal)
            # Coincidencias: 2 -> Multiplicador 1.2 (20% extra)
            # Coincidencias: 3 -> Multiplicador 1.4 (40% extra)
            cantidad_matches = conteo_coincidencias[peli_id]
            bonus_multiplier = 1.0 + (0.2 * (cantidad_matches - 1))
            
            score_final = score * bonus_multiplier

            ranking.append((score_final, titulo_obj, puntaje_obj))
            seen_ids.add(peli_id)
    
    # Ordenar por el score dopado
    ranking.sort(key=lambda x: x[0], reverse=True)
    
    # Debug
    print("\n🏆 Top 3 Ganadores (Con Bonus de Género):")
    for i, (sc, p, r) in enumerate(ranking[:3]):
        matches = conteo_coincidencias[p.id]
        print(f"   {i+1}. {p.titulo} (Matches: {matches}) - Score Final: {sc:.4f}")

    top_resultados = [(item[1], item[2]) for item in ranking[:top_k]]
    
    return top_resultados