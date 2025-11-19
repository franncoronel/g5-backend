from fastapi import APIRouter, Query
from sqlalchemy.orm import Session
from src.database.entidades import motor
from src.models.preferencia import PreferenciaDTO

# Importamos el servicio
from src.services.search_service import obtener_recomendaciones_hibridas

router = APIRouter()

@router.post("/preferencias")
def recibir_preferencias(
        preferenciaDTO: PreferenciaDTO,
        top_k: int = Query(20, ge=1, le=200),
        alpha: float = Query(0.8, ge=0.0, le=1.0)
    ):
    
    with Session(motor) as s:
        
        # Llamamos al servicio que devuelve [(Titulo, Puntaje), ...]
        resultados = obtener_recomendaciones_hibridas(preferenciaDTO, s, top_k)

        if not resultados:
            return {"items": [], "count": 0}

        items = []
        
        for i, (titulo, puntaje) in enumerate(resultados):
            
            # ✅ Extraemos Rating Real
            rating_real = puntaje.promedio if (puntaje and puntaje.promedio) else 0.0
            
            # Fecha segura
            anio = titulo.fecha_estreno.year if titulo.fecha_estreno else None

            simulated_score = 1.0 - (i / len(resultados))

            items.append({
                "id": titulo.id,
                "title": titulo.titulo,
                "year": anio,
                "duration": titulo.duracion,
                "poster": titulo.poster,
                "rating": rating_real, 
                "similarity": simulated_score,
                "score": simulated_score
            })

        return {"items": items, "count": len(items)}