'''
TODO:PARA CORRER EL CÓDIGO CON EL SIG. COMANDO EN TERMINAL -> 
      python -m src.data_analysis.titles
'''
import os
import sys 
import pandas as pd

# Ajustar path para poder importar módulos del proyecto
# Subo dos niveles desde data_analysis -> src -> g5-backend
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))

from src.paths import RUTA_TITULO
from src.paths import DIR_DATA_PROCESADA
from src.helpers import DataCleaner

def main():
  cleaner=DataCleaner(RUTA_TITULO, DIR_DATA_PROCESADA)

  # Tipos de películas que queremos mantener
  tipos_peliculas = {"titleType": ["movie", "tvMovie"]}

  df_peliculas=cleaner.limpiar(filtros=tipos_peliculas)

  # Columnas a verificar
  columnas_a_filtrar = ['genres', 'primaryTitle', 'originalTitle', 'runtimeMinutes']

  # Aplicar el filtro
  df_peliculas_limpio = cleaner.limpiar_nulos(df_peliculas, columnas_a_filtrar) 

  # Filtrar películas del 2019
  filtros={'startYear':'2019',
          'isAdult':0}

  df_peliculas_filtrado = cleaner.filtrar_dataframe(df_peliculas_limpio, filtros)

  # Convierto géneros a listas
  df_peliculas_filtrado = cleaner.columna_como_lista(df_peliculas_filtrado,'genres')

  # Extraigo todos los géneros únicos
  todos_los_generos = sorted(set(
        g for lista in df_peliculas_filtrado["genres"] if isinstance(lista, list)
        for g in lista))  
  
  df_generos = pd.DataFrame({"id_genre": range(1, len(todos_los_generos) + 1),"typeGenre": todos_los_generos})

  # Creo tabla relacional (película ↔ género)
  df_rel = df_peliculas_filtrado[["tconst", "genres"]].explode("genres").merge(
        df_generos,
        left_on="genres",
        right_on="typeGenre")[["tconst", "id_genre"]]
  
  # Elimino columnas no necesarias
  columnas_a_eliminar=["isAdult","genres"]  #, "endYear"
  df_peliculas_filtrado = cleaner.eliminar_columnas(df_peliculas_filtrado,columnas_a_eliminar)

  # Guardo archivos CSVs
  cleaner.guardar_csv(df_peliculas_filtrado, "peliculas_2019.csv")
  cleaner.guardar_csv(df_generos, "generos_2019.csv")
  cleaner.guardar_csv(df_rel, "rel_titulos_generos.csv")

if __name__ == "__main__":
    main()