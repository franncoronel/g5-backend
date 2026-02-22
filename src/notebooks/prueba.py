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
#     display_name: .venv (3.12.3)
#     language: python
#     name: python3
# ---

# %%
import os
import pandas as pd

def encontrar_raiz_proyecto(archivo_raiz="README.md") -> str:
    """Encuentra la raíz del proyecto buscando un archivo identificador"""
    ruta = os.path.abspath(os.getcwd())
    while True:
        if archivo_raiz in os.listdir(ruta):
            return ruta
        nueva_ruta = os.path.dirname(ruta)
        if nueva_ruta == ruta:  # Llegamos a la raíz del sistema sin encontrar
            raise FileNotFoundError(f"No se encontró {archivo_raiz} en ningún directorio padre")
        ruta = nueva_ruta

def leer_tsv_chunks(ruta: str):
    return pd.read_csv(ruta, sep='\t', chunksize=10000)


# %%
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

# %%
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

# Mostrar resultados
for tipo in tipos_buscados:
    print(f"\n=== {tipo.upper()} ===")
    print("Título Original | Año Inicio | Duración | Géneros")
    print("-" * 70)
    for registro in resultados[tipo]:
        print(f"{registro['originalTitle'][:30]:<30} | {registro['startYear']:<10} | {registro['runtimeMinutes']:<8} | {registro['genres']}")

# %%
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
print("\nDistribución por tipo:")
print(df_peliculas['titleType'].value_counts())

print("\nPrimeras 5 películas de cada tipo:")
for tipo in tipos_peliculas:
    print(f"\n=== {tipo.upper()} ===")
    print(df_peliculas[df_peliculas['titleType'] == tipo].head()[['primaryTitle', 'startYear', 'runtimeMinutes', 'genres']])


# %%
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

# %%
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

print("\nMuestra de 5 registros limpios:")
df_peliculas_limpio[['primaryTitle', 'titleType', 'startYear', 'runtimeMinutes', 'genres']].head()

# %%
# Filtrar películas del 2019
df_peliculas_filtrado = df_peliculas_limpio[df_peliculas_limpio['startYear'] == '2019']

print(f"Total de películas del 2019: {len(df_peliculas_filtrado):,}")
print("\nDistribución por tipo:")
print(df_peliculas_filtrado['titleType'].value_counts())

print("\nEstadísticas de duración (en minutos):")
print(df_peliculas_filtrado['runtimeMinutes'].astype(float).describe())

print("\nMuestra de películas del 2019:")
df_peliculas_filtrado.head(10)

ids_peliculas = df_peliculas_filtrado['tconst']



# %%
# Función para filtrar chunks basado en los IDs
def filtrar_por_ids(chunk):
    return chunk[chunk['tconst'].isin(ids_peliculas)]

# Filtrar tabla de críticas
print("Filtrando críticas...")
chunks_filtrados = []
criticas_iterable = leer_tsv_chunks(RUTA_CRITICAS)
for chunk in criticas_iterable:
    filtrado = filtrar_por_ids(chunk)
    if not filtrado.empty:
        chunks_filtrados.append(filtrado)
df_criticas_filtrado = pd.concat(chunks_filtrados, ignore_index=True) if chunks_filtrados else pd.DataFrame()


# Filtrar tabla de personal
print("Filtrando personal...")
chunks_filtrados = []
personal_iterable = leer_tsv_chunks(RUTA_PERSONAL)
for chunk in personal_iterable:
    filtrado = filtrar_por_ids(chunk)
    if not filtrado.empty:
        chunks_filtrados.append(filtrado)
df_personal_filtrado = pd.concat(chunks_filtrados, ignore_index=True) if chunks_filtrados else pd.DataFrame()

# Filtrar tabla de principales
print("Filtrando principales...")
chunks_filtrados = []
principales_iterable = leer_tsv_chunks(RUTA_PRINCIPALES)
for chunk in principales_iterable:
    filtrado = filtrar_por_ids(chunk)
    if not filtrado.empty:
        chunks_filtrados.append(filtrado)
df_principales_filtrado = pd.concat(chunks_filtrados, ignore_index=True) if chunks_filtrados else pd.DataFrame()

# Filtrar tabla de nombres
print("Filtrando nombres...")
chunks_filtrados = []
nombres_iterable = leer_tsv_chunks(RUTA_NOMBRE)
for chunk in nombres_iterable:
    filtrado = filtrar_por_ids(chunk)
    if not filtrado.empty:
        chunks_filtrados.append(filtrado)
df_nombres_filtrado = pd.concat(chunks_filtrados, ignore_index=True) if chunks_filtrados else pd.DataFrame()

# %%
# Guardar como CSV
ruta_salida = os.path.join(DIR_RAIZ, "data", "procesado")
os.makedirs(ruta_salida, exist_ok=True)

df_peliculas_filtrado.to_csv(os.path.join(ruta_salida, "peliculas_2019.csv"), index=False)
df_nombres_filtrado.to_csv(os.path.join(ruta_salida, "nombres_2019.csv"), index=False)
df_principales_filtrado.to_csv(os.path.join(ruta_salida, "principales_2019.csv"), index=False)
df_criticas_filtrado.to_csv(os.path.join(ruta_salida, "criticas_2019.csv"), index=False)
df_personal_filtrado.to_csv(os.path.join(ruta_salida, "personal_2019.csv"), index=False)

print("\nArchivos guardados en la carpeta 'data/procesado/'")
print("Muestra de los datos:")
print("\nPelículas:")
print(df_peliculas_filtrado.head())
print("\nCríticas:")
print(df_criticas_filtrado.head())
print("\nPersonal:")
print(df_personal_filtrado.head())
print("\nNombres:")
print(df_nombres_filtrado.head())
print("\nPrincipales:")
print(df_principales_filtrado.head())

# %%
# Conjunto para almacenar profesiones únicas
profesiones_unicas = set()

# Leer chunk por chunk
nombres_iterable = leer_tsv_chunks(RUTA_NOMBRE)
for chunk in nombres_iterable:
    # Filtrar filas donde primaryProfession no sea nulo o '\N'
    profesiones_validas = chunk[~chunk['primaryProfession'].isna() & (chunk['primaryProfession'] != '\\N')]
    
    # Para cada fila, dividir las profesiones y añadirlas al conjunto
    for profesiones in profesiones_validas['primaryProfession']:
        profesiones_unicas.update(profesiones.split(','))

# Convertir a lista y ordenar alfabéticamente
lista_profesiones = sorted(list(profesiones_unicas))
print(f"Total de profesiones únicas encontradas: {len(lista_profesiones)}")
print("\nLista de profesiones:")
for profesion in lista_profesiones:
    print(f"- {profesion}")

# %%
principales_iterable = leer_tsv_chunks(RUTA_PRINCIPALES)

ultimo_chunk = None
for chunk in principales_iterable:
    ultimo_chunk = chunk
    
ultimo_chunk.tail(10)

# %%
criticas_iterable = leer_tsv_chunks(RUTA_CRITICAS)

ultimo_chunk = None
for chunk in criticas_iterable:
    ultimo_chunk = chunk
    
ultimo_chunk.tail(10)


# %%
def direccionArchivo():
    absFilePath=os.path.abspath(__file__)
    path,filename=os.path.split(absFilePath)

    return path

def crearData():
    path=direccionArchivo()
    return pd.read_csv(path+"./mundial.csv")
