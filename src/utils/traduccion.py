import json
import os
from deep_translator import GoogleTranslator

from src.paths import DIR_CACHE

# Crear la carpeta si no existe
os.makedirs(DIR_CACHE, exist_ok=True)
CACHE_FILE = os.path.join(DIR_CACHE, "traducciones_generos.json")

# Cache persistente
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        _cache_traducciones = json.load(f)
else:
    _cache_traducciones = {}

def guardar_cache():
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(_cache_traducciones, f, ensure_ascii=False, indent=2)

def traducir_genero(nombre_genero: str) -> str:
    if nombre_genero in _cache_traducciones:
        return _cache_traducciones[nombre_genero]
    try:
        traducido = GoogleTranslator(source="en", target="es").translate(nombre_genero)
        _cache_traducciones[nombre_genero] = traducido
        guardar_cache()
        return traducido
    except Exception as e:
        print(f"⚠️ Falló la traducción de '{nombre_genero}': {e}")
        return nombre_genero
