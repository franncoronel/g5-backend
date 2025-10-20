import pandas as pd
from src.database.entidades import motor
from src.paths import RUTA_TITULO_2019, RUTA_ALIAS_2019, RUTA_CRITICAS_2019, RUTA_NOMBRE_2019, RUTA_PRINCIPALES_2019

# 2. Carga tu CSV limpio a un DataFrame de Pandas
df_titulos = pd.read_csv(RUTA_TITULO_2019)

df_titulos = df_titulos.drop('originalTitle', 'genres')

# ¡IMPORTANTE!
# Asegúrate de que los nombres de las columnas en tu CSV coincidan
# EXACTAMENTE con los nombres de las columnas en tu tabla de la base de datos.
# Si no coinciden, puedes renombrarlos en Pandas:
# df = df.rename(columns={'titulo_csv': 'nombre_columna_db'})

df_titulos = df_titulos.rename(columns={'tconst': 'id','titleType': 'tipo','primaryTitle':'titulo',})

# 3. Carga el DataFrame a la tabla
print("Cargando datos a la tabla 'titulos'...")
df_titulos.to_sql(
    'titulo',          # Nombre de la tabla en la BD
    con=motor,        # El motor de SQLAlchemy
    if_exists='append', # 'append' = añade los datos, 'replace' = borra y crea, 'fail' = falla si existe
    index=False        # No guardes el índice de Pandas como una columna
)
print("¡Carga completada!")