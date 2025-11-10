from fastapi import APIRouter
from src.models.preferencia import PreferenciaDTO

router = APIRouter()

@router.post("/preferencias")
def recibir_preferencias(preferencia: PreferenciaDTO):
    print("📩 Preferencias recibidas:")
    print(preferencia.model_dump())  # Versión en dict
    return {"mensaje": "Preferencias recibidas correctamente"}