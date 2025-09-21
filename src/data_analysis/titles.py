'''
TODO:PARA CORRER EL CÓDIGO CON EL SIG. COMANDO EN TERMINAL -> python -m src.data_analysis.titles
'''

import pandas as pd
import os
import sys 
import time

# Ajustar path para poder importar módulos del proyecto
# Subo dos niveles desde data_analysis -> src -> g5-backend
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))

from src.paths import RUTA_TITULO
from src.paths import DIR_DATA_PROCESADA
from src.helpers import leer_tsv_chunks


# Función para contar valores nulos y '\N'
def contar_nulos(df, columna):
  nulos_N = df[df[columna] == '\\N'].shape[0]  # Contar '\N'
  nulos_nan = df[columna].isna().sum()         # Contar NaN
  total = nulos_N + nulos_nan
  porcentaje = (total / len(df)) * 100
  return {
        'Valores \\N': nulos_N,
        'Valores NaN': nulos_nan,
        'Total Nulos': total,
        'Porcentaje': f"{porcentaje:.2f}%"
        }
# Función para guardar archivos
def guardar_csv(df, nombre_archivo):
  os.makedirs(DIR_DATA_PROCESADA, exist_ok=True)
  df.to_csv(os.path.join(DIR_DATA_PROCESADA, nombre_archivo), index=False, encoding="utf-8")
  print(f"Archivo guardado: {nombre_archivo}")



start = time.perf_counter()
print("Iniciando limpieza....\n\n")

'''Muestro la cantidad y tipos de títulos encontrados'''
titulos_iterable = leer_tsv_chunks(RUTA_TITULO)

# Conjunto para almacenar tipos únicos
tipos_unicos = set()

# Leer chunk por chunk y añadir los tipos únicos al conjunto
for chunk in titulos_iterable:
    tipos_unicos.update(chunk['titleType'].unique())

# Convertir a lista y ordenar alfabéticamente
lista_tipos = sorted(list(tipos_unicos))

print("Tipos de títulos únicos encontrados:")
for tipo in lista_tipos:
    print(f"- {tipo}")

print(f'\n Cantidad total de tipos de títulos: {len(lista_tipos)}')


'''Filtro 5 títulos de short, tvMovie, tvShort, tvSpecial'''
# Lista de tipos que queremos filtrar
tipos_buscados = ['short', 'tvMovie', 'tvShort', 'tvSpecial']

# Diccionario para almacenar los resultados de cada tipo
resultados = {tipo: [] for tipo in tipos_buscados}

# Leer chunks y filtrar
titulos_iterable = leer_tsv_chunks(RUTA_TITULO)

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
'''for tipo in tipos_buscados:
    print(f"\n=== {tipo.upper()} ===")
    header = f"{'Título Original':<35} | {'Año Inicio':<10} | {'Duración':<8} | Géneros"
    print(header)
    print("-" * len(header))
    
    for registro in resultados[tipo]:
        titulo = registro['originalTitle'][:35]  # Limitar a 35 caracteres
        anio = registro['startYear']
        duracion = registro['runtimeMinutes']
        generos = registro['genres']
        print(f"{titulo:<35} | {anio:<10} | {duracion:<8} | {generos}")'''

'''Filtramos sólo las películas.  
De todo el dataset, guarda solo películas y TV movies'''
# Tipos de películas que queremos mantener
tipos_peliculas = ['movie', 'tvMovie']

# Lista para ir acumulando los chunks filtrados
peliculas_filtradas = []

# Leer y filtrar por chunks
titulos_iterable = leer_tsv_chunks(RUTA_TITULO)
for chunk in titulos_iterable:
    # Filtrar solo los tipos que queremos
    chunk_filtrado = chunk[chunk['titleType'].isin(tipos_peliculas)]
    peliculas_filtradas.append(chunk_filtrado)

# Concatenar todos los chunks filtrados en un único DataFrame
df_peliculas = pd.concat(peliculas_filtradas, ignore_index=True)

# Mostrar información general
print(f"Total de registros filtrados: {len(df_peliculas)}")
'''print("\nDistribución por tipo:")
print(df_peliculas['titleType'].value_counts())

print("\nPrimeras 5 películas de cada tipo:")
for tipo in tipos_peliculas:
    print(f"\n=== {tipo.upper()} ===")
    print(df_peliculas[df_peliculas['titleType'] == tipo].head()[['primaryTitle', 'startYear', 'runtimeMinutes', 'genres']])'''


'''Recorre todas las columnas y muestra cuántos nulos hay en cada una.'''
# Analizar cada columna
print("Análisis de valores nulos por columna:")
print("-" * 50)

for columna in df_peliculas.columns:
    resultados = contar_nulos(df_peliculas, columna)
    print(f"\nColumna: {columna}")
    print(f"- Valores '\\N': {resultados['Valores \\N']:,}")
    print(f"- Valores NaN: {resultados['Valores NaN']:,}")
    print(f"- Total nulos: {resultados['Total Nulos']:,}")
    print(f"- Porcentaje: {resultados['Porcentaje']}")

# Mostrar también cuántos registros tienen al menos un valor nulo
registros_con_nulos = df_peliculas[df_peliculas.apply(lambda x: (x == '\\N').any() or x.isna().any(), axis=1)]
print(f"\nRegistros con al menos un valor nulo: {len(registros_con_nulos):,} ({(len(registros_con_nulos)/len(df_peliculas)*100):.2f}% del total)")

'''Limpieza de nulos.  
Se eliminan los registros donde falten datos en columnas clave.'''
# Columnas a verificar
columnas_a_filtrar = ['genres', 'primaryTitle', 'originalTitle', 'runtimeMinutes']

# Crear una máscara para filtrar
mascara = True  # Comenzamos con todos los registros
for columna in columnas_a_filtrar:
    # Filtrar tanto '\N' como NaN
    mascara = mascara & (df_peliculas[columna] != '\\N') & (~df_peliculas[columna].isna())

# Aplicar el filtro
df_peliculas_limpio = df_peliculas[mascara]

# Mostrar información sobre los registros filtrados
registros_eliminados = len(df_peliculas) - len(df_peliculas_limpio)
print(f"Registros originales: {len(df_peliculas):,}")
print(f"Registros después de eliminar nulos: {len(df_peliculas_limpio):,}")
print(f"Registros eliminados: {registros_eliminados:,} ({(registros_eliminados/len(df_peliculas)*100):.2f}%)")

print("\nDistribución por tipo después de la limpieza:")
print(df_peliculas_limpio['titleType'].value_counts())

'''print("\nMuestra de 5 registros limpios:")
df_peliculas_limpio[['primaryTitle', 'titleType', 'startYear', 'runtimeMinutes', 'genres']].head()'''


'''Filtra solo películas del año 2019 que no sean para adultos.'''
# Filtrar películas del 2019
df_peliculas_filtrado = df_peliculas_limpio[(df_peliculas_limpio['startYear'] == '2019') & 
                                            (df_peliculas_limpio['isAdult'] == 0)]
# Elimino la columna isAdult
df_peliculas_filtrado = df_peliculas_filtrado.drop(columns=["isAdult"])   #, "endYear"

print(f"Total de películas del 2019: {len(df_peliculas_filtrado):,}")
'''print("\nDistribución por tipo:")
print(df_peliculas_filtrado['titleType'].value_counts())

print("\nEstadísticas de duración (en minutos):")
print(df_peliculas_filtrado['runtimeMinutes'].astype(float).describe())

print("\nMuestra de películas del 2019:")
df_peliculas_filtrado.head(10)'''

guardar_csv(df_peliculas_filtrado, "peliculas_2019.csv")



suma = sum(range(10**6))

end = time.perf_counter()
print(f"Tiempo de ejecución: {end - start:.4f} segundos")