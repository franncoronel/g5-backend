from fastapi import APIRouter
from src.mappers import mapearPreferencia
from src.models.preferencia import PreferenciaDTO

router = APIRouter()

@router.post("/preferencias")
def recibir_preferencias(preferenciaDTO: PreferenciaDTO):
    print(preferenciaDTO)
    preferencia=mapearPreferencia(preferenciaDTO)
    print(preferencia)  # Versión en dict
    return {"mensaje": "Preferencias recibidas correctamente"}