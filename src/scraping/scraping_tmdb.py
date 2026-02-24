# Ejecutar con "python -m src.scraping.scraping_tmdb"

import os
import requests
from dotenv import load_dotenv
from pprint import pprint
load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")

if not API_KEY:
    raise ValueError("❌ No se encontró la clave TMDB_API_KEY en el archivo .env")

BASE_URL = "https://api.themoviedb.org/3"
IMG_BASE = "https://image.tmdb.org/t/p/original"

def buscar_pelicula(nombre):
    url = f"{BASE_URL}/search/movie"
    params = {
        "api_key": API_KEY,
        "query": nombre,
        "language": "es-ES"}
    r = requests.get(url, params=params)
    r.raise_for_status()
    datos = r.json()
    resultados = []
    for item in datos.get("results", [])[:3]:
        movie_id = item["id"]
        # (géneros, duración)
        detalles = obtener_detalles(movie_id)
        directores = obtener_directores(movie_id)
        resultados.append({
            "id": movie_id,
            "titulo": item.get("title"),
            "titulo_original": item.get("original_title"),
            "sinopsis": item.get("overview"),
            "idioma": item.get("original_language"),
            "fecha_estreno": item.get("release_date"),
            "poster_url": IMG_BASE + item["poster_path"] if item.get("poster_path") else None,
            "fondo_url": IMG_BASE + item["backdrop_path"] if item.get("backdrop_path") else None,
            "rating": item.get("vote_average"),
            "generos": detalles.get("generos"),
            "duracion": detalles.get("duracion"),
            "directores": directores,})
    return resultados

def obtener_detalles(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {"api_key": API_KEY,"language": "es-ES"}
    r = requests.get(url, params=params)
    r.raise_for_status()
    datos = r.json()
    return {"generos": [g["name"] for g in datos.get("genres", [])],
        "duracion": datos.get("runtime")}

def obtener_directores(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/credits"
    params = {"api_key": API_KEY}
    r = requests.get(url, params=params)
    r.raise_for_status()
    datos = r.json()
    return [p["name"] for p in datos.get("crew", []) if p.get("job") == "Director"]

if __name__ == "__main__":
    resultados = buscar_pelicula("Alita: Battle Angel")
    pprint(resultados)
