"""
Correr con:
    python -m src.data_analysis.ratings
"""
import os
import sys
import pandas as pd
# import uuid

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))

from src.paths import RUTA_CRITICAS, DIR_DATA_PROCESADA,RUTA_TITULO_2019
from src.helpers import DataCleaner

def main():
  # Cargo las películas 2019 procesadas
  peliculas_2019 = pd.read_csv(RUTA_TITULO_2019)
  ids_2019 = set(peliculas_2019['tconst'].astype(str))

  cleaner = DataCleaner(RUTA_CRITICAS, DIR_DATA_PROCESADA)
  
  columnas_ratings = ["tconst", "averageRating", "numVotes"]
  df_ratings = cleaner.limpiar(filtros={"tconst": list(ids_2019)})

  df_ratings = cleaner.mantener_columnas(df_ratings, columnas_ratings)

  # df_ratings['id'] = [str(uuid.uuid4()) for _ in range(len(df_ratings))]
  df_ratings['id'] = range(1, len(df_ratings) + 1) 
  df_ratings = df_ratings[['id', 'tconst', 'averageRating', 'numVotes']]
  
  cleaner.guardar_csv(df_ratings, "criticas_2019.csv")

if __name__ == "__main__":
  main()