# Ejecutar con "python -m src.scraping.enriquecer_titulos"
import os
import requests
import pandas as pd
from dotenv import load_dotenv
from time import sleep
from tqdm import tqdm
from src.paths import RUTA_TITULO_2019, DIR_DATA_PROCESADA

# ======== CONFIGURACION ========
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
if not API_KEY:
    raise ValueError("❌ Falta la clave TMDB_API_KEY en tu archivo .env")

BASE_URL = "https://api.themoviedb.org/3"
BLOQUE_GUARDADO = 100      # Guardar cada 100 películas procesadas
PAUSA = 1.0                # Pausa entre requests (segundos)
LIMITE_DIARIO = 2600       # Máximo de requests por ejecución 2750 x día
# ===============================


def buscar_pelicula(nombre, anio=None, idioma="es-ES"):
    """Busca una película en TMDB por nombre (y opcionalmente año)."""
    params = {"api_key": API_KEY, "query": nombre, "language": idioma}
    if anio:
        params["year"] = anio
    r = requests.get(f"{BASE_URL}/search/movie", params=params)
    if r.status_code != 200:
        return None
    data = r.json().get("results", [])
    return data[0] if data else None


def obtener_datos_tmdb(nombre, original, anio):
    """Obtiene información desde TMDB usando varios títulos e idiomas."""
    posibles_anios = [anio, int(anio) + 1, int(anio) + 2] if str(anio).isdigit() else [None]
    pelicula = None

    for a in posibles_anios:
        # Español
        pelicula = buscar_pelicula(nombre, a, idioma="es-ES")
        if pelicula:
            break
        pelicula = buscar_pelicula(original, a, idioma="es-ES")
        if pelicula:
            break
        # Inglés
        pelicula = buscar_pelicula(nombre, a, idioma="en-US")
        if pelicula:
            break

    if not pelicula:
        return None

    movie_id = pelicula["id"]
    sinopsis = pelicula.get("overview") or ""

    # Si no hay sinopsis en español, buscar en inglés
    if not sinopsis:
        r_en = requests.get(f"{BASE_URL}/movie/{movie_id}", params={"api_key": API_KEY, "language": "en-US"})
        if r_en.status_code == 200:
            sinopsis = r_en.json().get("overview", "")

    poster_path = pelicula.get("poster_path")
    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ""
    idioma_original = pelicula.get("original_language", "")
    fecha_estreno = pelicula.get("release_date", "")

    # Plataformas de streaming
    plataformas = "No disponible"
    r2 = requests.get(f"{BASE_URL}/movie/{movie_id}/watch/providers", params={"api_key": API_KEY})
    if r2.status_code == 200:
        provs = r2.json().get("results", {}).get("AR")
        if provs and "flatrate" in provs:
            plataformas = ", ".join(p["provider_name"] for p in provs["flatrate"])

    return {
        "id_tmdb": movie_id,
        "sinopsis": sinopsis,
        "poster": poster_url,
        "idioma_original": idioma_original,
        "plataformas": plataformas,
        "fecha_estreno": fecha_estreno
    }


def main():
    # Cargar dataset base
    df = pd.read_csv(RUTA_TITULO_2019)
    print(f"🎬 Total de títulos en el dataset: {len(df)}")

    ruta_ok = os.path.join(DIR_DATA_PROCESADA, "peliculas_cargadas.csv")
    ruta_no = os.path.join(DIR_DATA_PROCESADA, "peliculas_no_encontradas.csv")

    # 🔄 Reanudar si ya hay progreso previo
    procesados = set()
    if os.path.exists(ruta_ok):
        df_ok = pd.read_csv(ruta_ok)
        procesados = set(df_ok["tconst"].astype(str))
        df = df[~df["tconst"].astype(str).isin(procesados)]
        print(f"🔁 Reanudando desde {len(procesados)} procesados, quedan {len(df)}...")

    resultados, no_encontradas = [], []
    total_requests = 0

    for _, fila in tqdm(df.iterrows(), total=len(df), desc="Procesando películas", ncols=100):
        if total_requests >= LIMITE_DIARIO:
            print("⏸️ Límite diario alcanzado. Detén y continúa mañana para evitar bloqueo de API.")
            break

        nombre = fila["primaryTitle"]
        original = fila["originalTitle"]
        anio = fila["startYear"]

        try:
            datos = obtener_datos_tmdb(nombre, original, anio)
            total_requests += 1

            if datos:
                fila_actualizada = {
                    "tconst": fila["tconst"],
                    "titleType": fila["titleType"],
                    "primaryTitle": fila["primaryTitle"],
                    "startYear": fila["startYear"],
                    "fecha_estreno": datos["fecha_estreno"],
                    "id_tmdb": datos["id_tmdb"],
                    "sinopsis": datos["sinopsis"],
                    "poster": datos["poster"],
                    "idioma_original": datos["idioma_original"],
                    "plataformas": datos["plataformas"]
                }
            else:
                fila_actualizada = {
                    "tconst": fila["tconst"],
                    "titleType": fila["titleType"],
                    "primaryTitle": fila["primaryTitle"],
                    "startYear": fila["startYear"],
                    "fecha_estreno": "",
                    "id_tmdb": "",
                    "sinopsis": "",
                    "poster": "",
                    "idioma_original": "",
                    "plataformas": "No disponible"
                }
                no_encontradas.append(fila_actualizada)

            resultados.append(fila_actualizada)

        except Exception as e:
            print(f"⚠️ Error en '{nombre}': {e}")
            fila_error = {
                "tconst": fila["tconst"],
                "titleType": fila["titleType"],
                "primaryTitle": fila["primaryTitle"],
                "startYear": fila["startYear"],
                "fecha_estreno": "",
                "id_tmdb": "",
                "sinopsis": "",
                "poster": "",
                "idioma_original": "",
                "plataformas": "No disponible"
            }
            resultados.append(fila_error)
            no_encontradas.append(fila_error)

        # 💾 Guardado progresivo
        if len(resultados) % BLOQUE_GUARDADO == 0:
            print(f"💾 Guardando progreso ({len(resultados)} registros nuevos)...")
            pd.DataFrame(resultados).to_csv(
                ruta_ok,
                mode="a",
                header=not os.path.exists(ruta_ok),
                index=False,
                encoding="utf-8-sig"
            )
            pd.DataFrame(no_encontradas).to_csv(
                ruta_no,
                mode="a",
                header=not os.path.exists(ruta_no),
                index=False,
                encoding="utf-8-sig"
            )
            resultados.clear()
            no_encontradas.clear()

        sleep(PAUSA)

    # Guardar lo restante
    if resultados:
        pd.DataFrame(resultados).to_csv(
            ruta_ok, mode="a", header=not os.path.exists(ruta_ok), index=False, encoding="utf-8-sig"
        )
    if no_encontradas:
        pd.DataFrame(no_encontradas).to_csv(
            ruta_no, mode="a", header=not os.path.exists(ruta_no), index=False, encoding="utf-8-sig"
        )

    print(f"\n✅ Archivo generado: {ruta_ok}")
    print(f"📄 No encontradas: {ruta_no}")
    print(f"📊 Requests totales usados: {total_requests}")


if __name__ == "__main__":
    main()
