'''
TODO:PARA CORRER EL CÓDIGO CON EL SIG. COMANDO EN TERMINAL -> python -m src.data_analysis.titles
'''
import os
import sys 
import time

# Ajustar path para poder importar módulos del proyecto
# Subo dos niveles desde data_analysis -> src -> g5-backend
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))

from src.paths import RUTA_TITULO
from src.paths import DIR_DATA_PROCESADA
from src.helpers import DataCleaner


def main():
  start = time.perf_counter()
  print("Iniciando limpieza....\n\n")

  cleaner=DataCleaner(RUTA_TITULO, DIR_DATA_PROCESADA)

  lista_tipos=cleaner.valores_unicos_columna('titleType')

  print("Tipos de títulos únicos encontrados:")
  for tipo in lista_tipos:
      print(f"- {tipo}")

  print(f'\n Cantidad total de tipos de títulos: {len(lista_tipos)}')


  # Tipos de películas que queremos mantener
  tipos_peliculas = {"titleType": ["movie", "tvMovie"]}

  df_peliculas=cleaner.limpiar(filtros=tipos_peliculas)

  # Mostrar información general
  print(f"Total de registros filtrados: {len(df_peliculas)}")
  print("\nDistribución por tipo:")
  print(df_peliculas['titleType'].value_counts())

  # Analizar cada columna
  cleaner.mostrar_nulos(df_peliculas)

  # Columnas a verificar
  columnas_a_filtrar = ['genres', 'primaryTitle', 'originalTitle', 'runtimeMinutes']

  # Aplicar el filtro
  df_peliculas_limpio = cleaner.limpiar_nulos(df_peliculas, columnas_a_filtrar) 
  

  # Mostrar información sobre los registros filtrados
  registros_eliminados = len(df_peliculas) - len(df_peliculas_limpio)
  print(f"Registros originales: {len(df_peliculas):,}")
  print(f"Registros después de eliminar nulos: {len(df_peliculas_limpio):,}")
  print(f"Registros eliminados: {registros_eliminados:,} ({(registros_eliminados/len(df_peliculas)*100):.2f}%)")

  print("\nDistribución por tipo después de la limpieza:")
  print(df_peliculas_limpio['titleType'].value_counts())

  # Filtrar películas del 2019
  filtros={'startYear':'2019',
          'isAdult':0}

  df_peliculas_filtrado = cleaner.filtrar_dataframe(df_peliculas_limpio, filtros)

  print(f"Total de películas del 2019: {len(df_peliculas_filtrado):,}")
  print("\nDistribución por tipo:")
  print(df_peliculas_filtrado['titleType'].value_counts())

  print("\nEstadísticas de duración (en minutos):")
  print(df_peliculas_filtrado['runtimeMinutes'].astype(float).describe())

  columnas_a_eliminar=["isAdult"]  #, "endYear"
  df_peliculas_filtrado = cleaner.eliminar_columnas(df_peliculas_filtrado,columnas_a_eliminar)

  cleaner.guardar_csv(df_peliculas_filtrado, "peliculas_2019.csv")

  end = time.perf_counter()
  print(f"\n\nTiempo de ejecución: {end - start:.4f} segundos")

if __name__ == "__main__":
    main()