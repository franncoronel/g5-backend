# Ejecutar con: python -m src.scraping.obtener_backdrops
import os
import requests
import pandas as pd
from dotenv import load_dotenv
from time import sleep
from tqdm import tqdm
from src.paths import RUTA_PLATFORM, DIR_DATA

# ======== CONFIGURACIÓN ========
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
if not API_KEY:
    raise ValueError("❌ Falta la clave TMDB_API_KEY en tu archivo .env")

BASE_URL = "https://api.themoviedb.org/3"
BLOQUE_GUARDADO = 100      # Guardar cada 100 películas procesadas
PAUSA = 1                  # Pausa entre requests (segundos)
LIMITE_DIARIO = 2000       # Límite de requests diarios
# ===============================


def obtener_backdrop(movie_id, idioma="es-ES"):
    """Devuelve solo el backdrop de una película por su id de TMDB."""
    r = requests.get(f"{BASE_URL}/movie/{movie_id}", params={
        "api_key": API_KEY,
        "language": idioma
    })

    if r.status_code != 200:
        return None

    data = r.json()
    backdrop_path = data.get("backdrop_path")
    return f"https://image.tmdb.org/t/p/original{backdrop_path}" if backdrop_path else ""


def main():
    # Cargar dataset base
    df = pd.read_csv(RUTA_PLATFORM)
    total_inicial = len(df)
    print(f"🎬 Total de películas en dataset: {total_inicial}")

    ruta_ok = os.path.join(DIR_DATA, "peliculas_backdrops.csv")
    ruta_no = os.path.join(DIR_DATA, "peliculas_backdrops_no_encontradas.csv")

    # 🔄 Reanudar si ya hay progreso previo
    procesados = set()
    if os.path.exists(ruta_ok):
        df_ok = pd.read_csv(ruta_ok)
        procesados = set(df_ok["tconst"].astype(str))
        df = df[~df["tconst"].astype(str).isin(procesados)]
        print(f"🔁 Reanudando desde {len(procesados)} procesados, quedan {len(df)}...")

    resultados, no_encontradas = [], []
    total_requests = 0
    total_procesados = len(procesados)

    for _, fila in tqdm(df.iterrows(), total=len(df), desc="Procesando películas", ncols=100):

        if total_requests >= LIMITE_DIARIO:
            print("⏸️ Límite diario alcanzado. Detén y continúa mañana.")
            break

        movie_id = fila.get("id_tmdb")
        if pd.isna(movie_id) or movie_id == "":
            continue

        try:
            backdrop = obtener_backdrop(int(movie_id))
            total_requests += 1
            total_procesados += 1

            fila_actualizada = {
                "tconst": fila["tconst"],
                "primaryTitle": fila["primaryTitle"],
                "id_tmdb": movie_id,
                "backdrop": backdrop or ""
            }

            if backdrop:
                resultados.append(fila_actualizada)
            else:
                no_encontradas.append(fila_actualizada)
                resultados.append(fila_actualizada)

        except Exception as e:
            print(f"⚠️ Error con ID {movie_id}: {e}")
            fila_error = {
                "tconst": fila["tconst"],
                "primaryTitle": fila["primaryTitle"],
                "id_tmdb": movie_id,
                "backdrop": ""
            }
            resultados.append(fila_error)
            no_encontradas.append(fila_error)

        # 💾 Guardado progresivo
        if len(resultados) % BLOQUE_GUARDADO == 0:
            faltantes = total_inicial - total_procesados
            print(f"💾 Guardando progreso ({len(resultados)} nuevos)... "
                  f"→ Procesados: {total_procesados} / {total_inicial} | Faltan: {faltantes}")

            # Guardar progreso principal
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

    # Guardar lo restante al final
    if resultados:
        pd.DataFrame(resultados).to_csv(
            ruta_ok, mode="a", header=not os.path.exists(ruta_ok), index=False, encoding="utf-8-sig"
        )
    if no_encontradas:
        pd.DataFrame(no_encontradas).to_csv(
            ruta_no, mode="a", header=not os.path.exists(ruta_no), index=False, encoding="utf-8-sig"
        )

    faltantes = total_inicial - total_procesados
    print(f"\n✅ Archivo generado: {ruta_ok}")
    print(f"📄 No encontradas: {ruta_no}")
    print(f"📊 Requests totales usados: {total_requests}")
    print(f"📈 Películas procesadas: {total_procesados} / {total_inicial} | Faltan {faltantes}")


if __name__ == "__main__":
    main()
