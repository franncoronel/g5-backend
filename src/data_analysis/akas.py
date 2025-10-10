"""
Correr con:
    python -m src.data_analysis.akas
"""

import os
import sys
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))

from src.paths import RUTA_ALIAS, DIR_DATA_PROCESADA, RUTA_TITULO_2019
from src.helpers import DataCleaner

def main():
    # Cargo las películas 2019 procesadas
    peliculas_2019 = pd.read_csv(RUTA_TITULO_2019)
    ids_2019 = set(peliculas_2019['tconst'].astype(str))

    cleaner = DataCleaner(RUTA_ALIAS, DIR_DATA_PROCESADA)

    columnas_a_mantener = ["titleId", "title", "isOriginalTitle", "region", "language"]

    # Filtrar por IDs relevantes
    df_akas = cleaner.limpiar(filtros={"titleId": list(ids_2019)})

    # Mantener columnas de interés y renombrar
    df_akas = cleaner.mantener_columnas(df_akas, columnas_a_mantener)
    df_akas = df_akas.rename(columns={"titleId": "tconst"})

    # 🔹 1. Mantener registros: si language es nulo pero isOriginalTitle == 1, conservar igual
    # Caso contrario (isOriginalTitle == 0 y language nulo), eliminar
    mascara_valida = (df_akas["language"].notna()) | (df_akas["isOriginalTitle"] == 1)
    df_akas = df_akas[mascara_valida].copy()

    # 🔹 2. Ordenar priorizando isOriginalTitle == 1 para que quede primero en los duplicados
    df_akas = df_akas.sort_values(
        by=["tconst", "isOriginalTitle", "language"],
        ascending=[True, False, True]  # primero originales, luego resto
    )

    # 🔹 3. Eliminar duplicados priorizando el original
    df_akas = df_akas.drop_duplicates(subset=["tconst", "language"], keep="first")
    df_akas = df_akas.drop_duplicates(subset=["tconst", "title"], keep="first")

    # Guardar archivo final (sobrescribiendo)
    cleaner.guardar_csv(df_akas, "alias_2019.csv")

if __name__ == "__main__":
    main()