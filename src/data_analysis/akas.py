"""
Correr con:
    python -m src.data_analysis.akas
"""

import os
import sys
import pandas as pd


sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))

from src.paths import RUTA_ALIAS, DIR_DATA_PROCESADA,RUTA_TITULO_2019
from src.helpers import DataCleaner

def main():
  # Cargo las películas 2019 procesadas
  peliculas_2019 = pd.read_csv(RUTA_TITULO_2019)
  ids_2019 = set(peliculas_2019['tconst'].astype(str))

  # print(f"Películas cargadas: {len(peliculas_2019):,}")
  # print(f"IDs únicos: {len(ids_2019):,}")

  cleaner = DataCleaner(RUTA_ALIAS, DIR_DATA_PROCESADA)

  columnas_a_mantener = ["titleId", "title", "isOriginalTitle", "region", "language"]

  df_akas = cleaner.limpiar(filtros={"titleId": list(ids_2019)})
  # print(f"Filtrado akas -> {len(df_akas):,} registros")

  df_akas = cleaner.mantener_columnas(df_akas, columnas_a_mantener)

  # Guardo Archivo
  cleaner.guardar_csv(df_akas, "alias_2019.csv")

if __name__ == "__main__":
    main()