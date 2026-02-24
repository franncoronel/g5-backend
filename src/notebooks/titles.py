# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: .venv
#     language: python
#     name: python3
# ---

# %%
import pandas as pd
import os
import sys
import importlib

# %%
# Subo dos niveles desde data_analysis -> src -> g5-backend
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))

# %%
from src.paths import RUTA_TITULO
from src.paths import DIR_DATA_PROCESADA
#from src.helpers import leer_tsv_chunks


# #! Lo siguiente es para que me tome los cambios realizados mientras actualizo la clase
import src.helpers
importlib.reload(src.helpers)
from src.helpers import DataCleaner

# %%
from src.paths import RUTA_PERSONAL
from src.paths import RUTA_CRITICAS
from src.paths import RUTA_PRINCIPALES
from src.paths import RUTA_NOMBRE

# %% [markdown]
# Muestro la cantidad y tipos de títulos encontrados

# %%
cleaner=DataCleaner(RUTA_TITULO, DIR_DATA_PROCESADA)

# %%
lista_tipos=cleaner.valores_unicos_columna('titleType')

print("Tipos de títulos únicos encontrados:")
for tipo in lista_tipos:
    print(f"- {tipo}")

print(f'\n Cantidad total de tipos de títulos: {len(lista_tipos)}')

# %% [markdown]
# Filtro 5 títulos de *short, tvMovie, tvShort, tvSpecial*

# %%
# Lista de tipos que queremos filtrar
tipos_buscados = ['short', 'tvMovie', 'tvShort', 'tvSpecial']

# Diccionario para almacenar los resultados de cada tipo
resultados = {tipo: [] for tipo in tipos_buscados}

# Leer chunks y filtrar
titulos_iterable = cleaner.leer_tsv_chunks(cleaner.ruta_archivo)

for chunk in titulos_iterable:
    for tipo in tipos_buscados:
        # Si aún no tenemos 5 registros de este tipo, buscamos más
        if len(resultados[tipo]) < 5:
            filtrados = chunk[chunk['titleType'] == tipo]
            # Tomamos solo los que faltan hasta llegar a 5
            resultados[tipo].extend(filtrados.head(5 - len(resultados[tipo])).to_dict('records'))

    # Verificar si ya tenemos 5 de cada tipo
    if all(len(registros) >= 5 for registros in resultados.values()):
        break

# Mostrar resultados con tabla alineada
for tipo in tipos_buscados:
    print(f"\n=== {tipo.upper()} ===")
    header = f"{'Título Original':<35} | {'Año Inicio':<10} | {'Duración':<8} | Géneros"
    print(header)
    print("-" * len(header))

    for registro in resultados[tipo]:
        titulo = registro['originalTitle'][:35]  # Limitar a 35 caracteres
        anio = registro['startYear']
        duracion = registro['runtimeMinutes']
        generos = registro['genres']
        print(f"{titulo:<35} | {anio:<10} | {duracion:<8} | {generos}")

# %% [markdown]
# Filtramos sólo las películas.  
# De todo el dataset, guarda solo películas y TV movies

# %%
# Tipos de películas que queremos mantener
tipos_peliculas = {"titleType": ["movie", "tvMovie"]}

df_peliculas=cleaner.limpiar(filtros=tipos_peliculas)

# Mostrar información general
print(f"Total de registros filtrados: {len(df_peliculas)}")
print("\nDistribución por tipo:")
print(df_peliculas['titleType'].value_counts())

# %%
print("\nPrimeras 5 películas de cada tipo:")
for tipo in tipos_peliculas["titleType"]:
    print(f"\n=== {tipo.upper()} ===")
    print(df_peliculas[df_peliculas['titleType'] == tipo].head()[['primaryTitle', 'startYear', 'runtimeMinutes', 'genres']])

# %% [markdown]
# Recorre todas las columnas y muestra cuántos nulos hay en cada una.

# %%
# Analizar cada columna
cleaner.mostrar_nulos(df_peliculas)

# %% [markdown]
# Limpieza de nulos.  
# Se eliminan los registros donde falten datos en columnas clave.

# %%
# Columnas a verificar
columnas_a_filtrar = ['genres', 'primaryTitle', 'originalTitle', 'runtimeMinutes']

# Aplicar el filtro
df_peliculas_limpio = cleaner.limpiar_nulos(df_peliculas, columnas_a_filtrar)

# %%
# Mostrar información sobre los registros filtrados
cleaner.mostrar_registros_filtrados(df_peliculas,df_peliculas_limpio)

print("\nDistribución por tipo después de la limpieza:")
print(df_peliculas_limpio['titleType'].value_counts())

print("\nMuestra de 5 registros limpios:")
df_peliculas_limpio[['primaryTitle', 'titleType', 'startYear', 'runtimeMinutes', 'genres']].head()

# %% [markdown]
# Filtra solo películas del año 2019 que no sean para adultos.

# %%
# Filtrar películas del 2019
filtros={'startYear':'2019',
        'isAdult':0}

df_peliculas_filtrado = cleaner.filtrar_dataframe(df_peliculas_limpio, filtros)

# %%
print(f"Total de películas del 2019: {len(df_peliculas_filtrado):,}")
print("\nDistribución por tipo:")
print(df_peliculas_filtrado['titleType'].value_counts())

print("\nEstadísticas de duración (en minutos):")
print(df_peliculas_filtrado['runtimeMinutes'].astype(float).describe())


# %%
columnas_a_eliminar=["isAdult"]  #, "endYear"
df_peliculas_filtrado = cleaner.eliminar_columnas(df_peliculas_filtrado,columnas_a_eliminar)

print("\nMuestra de películas del 2019:")
df_peliculas_filtrado.head(10)

# %%
cleaner.guardar_csv(df_peliculas_filtrado, "peliculas_2019.csv")

# %% [markdown]
# ### Creo archivo para alias (title.akas.tsv)

# %%
import src.paths
import src.helpers
importlib.reload(src.paths)
importlib.reload(src.helpers)

# %%
from src.helpers import DatasetManager

# %%
from src.paths import RUTA_ALIAS
from src.paths import RUTA_TITULO_2019
from src.paths import RUTA_CRITICAS

# %%
dm = DatasetManager()
preview = dm.ver_preview(RUTA_ALIAS, n=4)

# %%
peliculas_2019 = pd.read_csv(RUTA_TITULO_2019)
print(f"Películas cargadas: {len(peliculas_2019):,}")
peliculas_2019.head()

# %%
print(peliculas_2019.columns.tolist())

# %%
ids_2019 = set(peliculas_2019['tconst'].astype(str))

print(f"Películas cargadas: {len(peliculas_2019):,}")
print(f"IDs únicos: {len(ids_2019):,}")

cleaner = DataCleaner(RUTA_ALIAS, DIR_DATA_PROCESADA)

# %%
columnas_a_mantener = ["titleId", "title", "isOriginalTitle", "region", "language"]

# %%
df_akas = cleaner.limpiar(filtros={"titleId": list(ids_2019)})
print(f"Filtrado akas -> {len(df_akas):,} registros")

# %%
df_akas = cleaner.mantener_columnas(df_akas, columnas_a_mantener)

# %%
df_akas = df_akas.rename(columns={"titleId": 'tconst'})

# %%
print(peliculas_2019.columns.tolist())
print(df_akas.columns.tolist())

# %%
cleaner.guardar_csv(df_akas, "alias_2019.csv")

# %%
ruta_alias = os.path.join(DIR_DATA_PROCESADA, "alias_2019.csv")
alias_2019 = pd.read_csv(ruta_alias)

print(alias_2019.columns.tolist())

# %%
ids_alias = set(alias_2019["titleId"].astype(str))
ids_peliculas = set(peliculas_2019["tconst"].astype(str))

print(f"Películas cargadas: {len(peliculas_2019):,}")
print(f"IDs únicos en películas: {len(ids_peliculas):,}")
print(f"Registros en alias: {len(alias_2019):,}")
print(f"IDs únicos en alias: {len(ids_alias):,}")

# Intersección (para verificar que coincidan)
ids_en_ambos = ids_peliculas.intersection(ids_alias)
print(f"IDs en ambos datasets: {len(ids_en_ambos):,}")

# %%
# Porcentaje de películas que tienen al menos un alias
cobertura = (len(ids_en_ambos) / len(ids_peliculas)) * 100
print(f"Cobertura de alias sobre películas: {cobertura:.2f}%")

# Porcentaje de alias que corresponden a alguna película de 2019
cobertura_alias = (len(ids_en_ambos) / len(ids_alias)) * 100
print(f"Cobertura de alias respecto a películas: {cobertura_alias:.2f}%")

# %% [markdown]
# ### Creo archivo para raitings (title.ratings.tsv)

# %%
peliculas_2019 = pd.read_csv(RUTA_TITULO_2019)
ids_2019 = set(peliculas_2019["tconst"].astype(str))

# %%
cleaner = DataCleaner(RUTA_CRITICAS, DIR_DATA_PROCESADA)

# %%
columnas_ratings = ["tconst", "averageRating", "numVotes"]
df_ratings = cleaner.limpiar(filtros={"tconst": list(ids_2019)})

# %%
df_ratings = cleaner.mantener_columnas(df_ratings, columnas_ratings)

# %%
cleaner.guardar_csv(df_ratings, "criticas_2019.csv")

# %%
# Información de verificación
print(f"Registros de Ratings filtrados: {len(df_ratings):,}")
print(f"IDs únicos en Ratings: {df_ratings['tconst'].nunique():,}")

# %% [markdown]
# ### Creo archivo para principals (title.principals.tsv.gz)

# %%
from src.paths import RUTA_PRINCIPALES
from src.paths import RUTA_TITULO_2019

from src.helpers import DatasetManager

# %%
peliculas_2019 = pd.read_csv(RUTA_TITULO_2019)
ids_2019 = set(peliculas_2019["tconst"].astype(str))

# %%
print(f"Películas cargadas: {len(peliculas_2019):,}")
print(f"IDs únicos: {len(ids_2019):,}")

# %%
cleaner = DataCleaner(RUTA_PRINCIPALES, DIR_DATA_PROCESADA)

# %%
dm = DatasetManager()
preview = dm.ver_preview(RUTA_PRINCIPALES, n=4)

# %%
columnas_a_mantener = ["tconst", "nconst", "category", "characters"]
listado_trabajos=["actor", "actress", "self", "director", "writer","composer","producer"]

# %%
df_principals = cleaner.limpiar(filtros={"tconst": list(ids_2019),
                                         "category":listado_trabajos})
print(f"Filtrado principals -> {len(df_principals):,} registros")

# %%
trabajos_unicos = set(df_principals["category"].dropna())
print("Tipos de Trabajos únicos encontrados:")
for tipo in trabajos_unicos:
    print(f"- {tipo}")

print(f'\n Cantidad total de tipos de títulos: {len(trabajos_unicos)}')

# %%
print(f"Registros de Principals filtrados: {len(df_principals):,}")
print(f"IDs únicos en Principals: {df_principals['tconst'].nunique():,}")

# %%
df_principals = cleaner.mantener_columnas(df_principals, columnas_a_mantener)

# %%
print(df_principals.columns.tolist())

# %%
cleaner.guardar_csv(df_principals, "principales_2019.csv")

# %%
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "./.")))
from src.paths import DIR_DATA_PROCESADA

# %%
RUTA_PRINCIPALS_2019 =os.path.join(DIR_DATA_PROCESADA,"principales_2019.csv")
dm = DatasetManager()
preview = dm.ver_preview(RUTA_PRINCIPALS_2019, n=4)

# %% [markdown]
# ### Creo archivo para names (name.basics.tsv.gz)

# %%
import src.paths
import src.helpers

# %%
importlib.reload(src.paths)
importlib.reload(src.helpers)

# %%
from src.paths import RUTA_NOMBRE
from src.paths import RUTA_PRINCIPALES_2019
from src.paths import RUTA_TITULO_2019

from src.helpers import DatasetManager
from src.helpers import DataCleaner

# %%
dm = DatasetManager()
preview = dm.ver_preview(RUTA_NOMBRE, n=4)

# %%
df_principals = pd.read_csv(RUTA_PRINCIPALES_2019)  #de aca saco los "nconst"

# %%
cleaner = DataCleaner(RUTA_NOMBRE , DIR_DATA_PROCESADA)

# %%
columnas_a_mantener = ['nconst', 'primaryName', 'birthYear','primaryProfession']#, 'knownForTitles'

# %%
nconsts_relevantes = set(df_principals["nconst"].astype(str))
print(f"Personas únicas en principals: {len(nconsts_relevantes):,}")

# %%
df_names = cleaner.limpiar(filtros={'nconst': list(nconsts_relevantes)})

# %%
print(f"Registros de names filtrados: {len(df_names):,}")
print(f"IDs únicos en names: {df_names['nconst'].nunique():,}")

# %%
df_names = cleaner.mantener_columnas(df_names,columnas_a_mantener)

# %%
cleaner.guardar_csv(df_names, "nombres_2019.csv")

# %%
from src.paths import RUTA_NOMBRE_2019

# %%
dm = DatasetManager()
preview = dm.ver_preview(RUTA_NOMBRE_2019, n=4)
