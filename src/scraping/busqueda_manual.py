# Ejecutar con python -m src.scraping.busqueda_manual

import os
import requests
import pandas as pd
from dotenv import load_dotenv
from time import sleep

# ======== CONFIGURACIÓN ========
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

if not API_KEY:
    raise ValueError("❌ Falta la clave TMDB_API_KEY en tu archivo .env")

BASE_URL = "https://api.themoviedb.org/3"
DIR_SALIDA = "data/procesada"
os.makedirs(DIR_SALIDA, exist_ok=True)
RUTA_OK = os.path.join(DIR_SALIDA, "peliculas_manual_ok.csv")
PAUSA = 1.0  # segundos entre requests
# ===============================


def buscar_pelicula(nombre, anio=None, idioma="es-ES"):
    """Busca una película en TMDB por nombre y año opcional."""
    params = {"api_key": API_KEY, "query": nombre, "language": idioma}
    if anio:
      params["year"] = anio

    try:
        resp = requests.get(f"{BASE_URL}/search/movie", params=params)
        if resp.status_code == 200:
            data = resp.json()
            resultados = data.get("results", [])
            if resultados:
                return resultados[0]  # la coincidencia más cercana
    except Exception as e:
        print(f"❌ Error buscando '{nombre}': {e}")

    return None


def obtener_datos_tmdb(nombre, original=None, anio=None, id_tmdb=None):
    """Obtiene sinopsis, poster, idioma original y plataformas."""
    pelicula = None

    # 1️⃣ Si tengo id_tmdb, voy directo
    if id_tmdb:
        r = requests.get(f"{BASE_URL}/movie/{id_tmdb}", params={"api_key": API_KEY, "language": "es-ES"})
        if r.status_code == 200:
            pelicula = r.json()
        else:
            print(f"⚠️ No se encontró ID TMDB {id_tmdb}")

    # 2️⃣ Si no tengo ID, busco por título
    if not pelicula:
        posibles_anios = []
        if anio and str(anio).isdigit():
            posibles_anios = [anio, int(anio) + 1, int(anio) + 2]
        else:
            posibles_anios = [None]

        for a in posibles_anios:
            pelicula = buscar_pelicula(nombre, a, idioma="es-ES")
            if pelicula:
                break
            if original:
                pelicula = buscar_pelicula(original, a, idioma="es-ES")
                if pelicula:
                    break
            pelicula = buscar_pelicula(nombre, a, idioma="en-US")
            if pelicula:
                break

    # 3️⃣ Si no encontré nada
    if not pelicula:
        print(f"❌ No se encontró información para '{nombre}'")
        return None

    movie_id = pelicula["id"]

    # --- Sinopsis ---
    sinopsis = pelicula.get("overview", "")
    if not sinopsis:
        # Buscar en inglés si no hay en español
        r_en = requests.get(f"{BASE_URL}/movie/{movie_id}", params={"api_key": API_KEY, "language": "en-US"})
        if r_en.status_code == 200:
            sinopsis = r_en.json().get("overview", "")
    if not sinopsis:
        sinopsis = f"Sinopsis no disponible para {nombre}."

    # --- Poster ---
    poster_path = pelicula.get("poster_path")
    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ""

    # --- Idioma original ---
    idioma_original = pelicula.get("original_language", "")

    # --- Plataformas ---
    plataformas = "No disponible"
    r2 = requests.get(f"{BASE_URL}/movie/{movie_id}/watch/providers", params={"api_key": API_KEY})
    if r2.status_code == 200:
        provs = r2.json().get("results", {}).get("AR")
        if provs and "flatrate" in provs:
            plataformas = ", ".join(p["provider_name"] for p in provs["flatrate"])
    
    fecha_estreno = pelicula.get("release_date", "")
    sleep(PAUSA)

    return {
        "id_tmdb": movie_id,
        "sinopsis": sinopsis,
        "poster": poster_url,
        "idioma_original": idioma_original,
        "plataformas": plataformas,
        "fecha_estreno": fecha_estreno
    }


# ===============================
# 🧩 Carga manual de películas
# ===============================

peliculas_a_buscar = [
    {
        "primaryTitle": "",
        "originalTitle": "",
        "startYear": 2019,
        "id_tmdb": ""
    },
    {
        "primaryTitle": "",
        "originalTitle": "",
        "startYear": 2019,
        "id_tmdb": ""
    },
]


resultados = []

for fila in peliculas_a_buscar:
    nombre = fila["primaryTitle"]
    original = fila.get("originalTitle")
    anio = fila.get("startYear")
    id_tmdb = fila.get("id_tmdb")

    print(f"\n🔍 Buscando '{nombre}' ({anio})...")
    datos = obtener_datos_tmdb(nombre, original, anio, id_tmdb)

    if datos:
        fila_actualizada = {
            "primaryTitle": nombre,
            "originalTitle": original,
            "startYear": anio,
            "id_tmdb": datos.get("id_tmdb", ""),
            "sinopsis": datos.get("sinopsis", ""),
            "poster": datos.get("poster", ""),
            "idioma_original": datos.get("idioma_original", ""),
            "plataformas": datos.get("plataformas", ""),
            "fecha_estreno": datos.get("fecha_estreno", ""),
        }
    else:
        # Si no encontró nada, igual agregamos la fila vacía para mantener columnas
        fila_actualizada = {
            "primaryTitle": nombre,
            "originalTitle": original,
            "startYear": anio,
            "id_tmdb": "",
            "sinopsis": "",
            "poster": "",
            "idioma_original": "",
            "plataformas": "",
            "fecha_estreno": "",
        }

    resultados.append(fila_actualizada)

# Guardar resultados
pd.DataFrame(resultados).to_csv(RUTA_OK, index=False, encoding="utf-8-sig")
print(f"\n✅ Datos guardados en: {RUTA_OK}")
