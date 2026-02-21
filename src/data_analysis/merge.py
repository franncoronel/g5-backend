"""
Correr con:
    python -m src.data_analysis.merge
"""
'''
* Correr sí y solo sí no se tiene el archivo 'peliculas_cargadas_actualizado.csv'
  En el caso de no ternerlo, 

Script es para hacer merge entre el archivo que contiene la info de la plataforma, poster, 
sinopsis, idioma_original, etc. , con el archivo que contiene los backdrops de las películas.

Solo se ejecuta si se lanzaron por separado los scripts de scraping para obtener_backdrops.py y enriquecer_titulos.py.

El resultado es un nuevo archivo csv con la info combinada → peliculas_cargadas_actualizado.csv → RUTA_PELICULAS_TMDB (path)

'''

import pandas as pd
import os
from src.paths import RUTA_PLATFORM, DIR_DATA_PROCESADA, RUTA_BACKDROPS

# Carga archivos
df_main = pd.read_csv(RUTA_PLATFORM, sep=",", low_memory=False)
df_backdrops = pd.read_csv(RUTA_BACKDROPS, sep=",")

# columnas importantes
df_backdrops = df_backdrops[["tconst", "backdrop"]]

# Merge LEFT JOIN
df_merged = df_main.merge(df_backdrops, on="tconst", how="left")

# Crear carpeta processed si no existe
os.makedirs(DIR_DATA_PROCESADA, exist_ok=True)

# Guardar archivo procesado sin tocar el original
ruta_salida = os.path.join(DIR_DATA_PROCESADA, "peliculas_cargadas_actualizado.csv")
df_merged.to_csv(ruta_salida, index=False, sep=",", encoding="utf-8-sig")

# Estadísticas
total = len(df_main)
con_backdrop = df_merged["backdrop"].notna().sum()
sin_backdrop = total - con_backdrop

print("\n✅ MERGE COMPLETO")
print(f"🎬 Total de registros en plataforma: {total}")
print(f"🖼️ Con backdrop agregado: {con_backdrop}")
print(f"🚫 Sin backdrop disponible: {sin_backdrop}")
print(f"📁 Archivo actualizado guardado en: {ruta_salida}")
