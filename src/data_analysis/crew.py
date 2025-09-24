# src/data_analysis/crew.py
"""
Correr con:
    python -m src.data_analysis.crew
"""

import os
import sys
import pandas as pd

# Dejar el import “desde la raíz” como en titles.py
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "./.")))

from src.paths import DIR_DATA_PROCESADA
try:
    # si ya agregaste esta constante en paths.py, la usamos
    from src.paths import RUTA_PERSONAL as RUTA_CREW
except ImportError:
    # fallback: construimos la ruta al archivo TSV dentro de /data
    from src.paths import BASE_DIR  # o ROOT_DIR si lo tenés
    ROOT_DIR = os.path.dirname(BASE_DIR)
    RUTA_CREW = os.path.join(ROOT_DIR, "data", "title.crew.tsv")  # o .tsv.gz

# Si tu helpers.py ya soporta gzip, usamos la misma función que en titles.py
try:
    from src.helpers import leer_tsv_chunks
except Exception:
    # fallback simple con compresión “infer”
    def leer_tsv_chunks(ruta):
        compression = "gzip" if ruta.endswith(".gz") else "infer"
        return pd.read_csv(ruta, sep="\t", chunksize=10000, compression=compression)

def main():
    # 1) Cargar IDs de películas 2019
    ruta_peliculas = os.path.join(DIR_DATA_PROCESADA, "peliculas_2019.csv")
    if not os.path.exists(ruta_peliculas):
        raise FileNotFoundError(f"No se encontró {ruta_peliculas}. Ejecutá primero titles.py para generar peliculas_2019.csv")

    peliculas_2019 = pd.read_csv(ruta_peliculas, dtype=str)
    ids_2019 = set(peliculas_2019["tconst"].astype(str))

    # 2) Filtrar crew.tsv por tconst ∈ ids_2019 (en chunks)
    filtrados = []
    for chunk in leer_tsv_chunks(RUTA_CREW):
        chunk["tconst"] = chunk["tconst"].astype(str)
        filtrados.append(chunk[chunk["tconst"].isin(ids_2019)])

    if len(filtrados) == 0:
        df_crew_2019 = pd.DataFrame(columns=["tconst", "directors", "writers"])
    else:
        df_crew_2019 = pd.concat(filtrados, ignore_index=True)

    # Opcional: reemplazar '\N' por NaN para limpiar
    df_crew_2019 = df_crew_2019.replace({"\\N": pd.NA})

    # 3) Guardar resultado junto al resto de procesados
    os.makedirs(DIR_DATA_PROCESADA, exist_ok=True)
    salida = os.path.join(DIR_DATA_PROCESADA, "crew_2019.csv")
    df_crew_2019.to_csv(salida, index=False, encoding="utf-8")
    print(f"Filas crew 2019: {len(df_crew_2019):,}")
    print(f"Archivo guardado: {salida}")

if __name__ == "__main__":
    main()
