# Ejecutar con "python -m scripts.data_loaders.names"

import pandas as pd
from src.database.entidades import motor
from src.paths import RUTA_NOMBRE_2019

# 2. Carga tu CSV limpio a un DataFrame de Pandas
df_nombres = pd.read_csv(RUTA_NOMBRE_2019)

# ¡IMPORTANTE!
# Asegúrate de que los nombres de las columnas en tu CSV coincidan
# EXACTAMENTE con los nombres de las columnas en tu tabla de la base de datos.
# Si no coinciden, puedes renombrarlos en Pandas:
# df = df.rename(columns={'titulo_csv': 'nombre_columna_db'})

df_nombres = df_nombres.rename(columns={'nconst': 'id','primaryName': 'nombre'})

# 3. Carga el DataFrame a la tabla
print("Cargando datos a la tabla 'persona'...")
df_nombres.to_sql(
    'persona',          # Nombre de la tabla en la BD
    con=motor,        # El motor de SQLAlchemy
    if_exists='replace', # 'append' = añade los datos, 'replace' = borra y crea, 'fail' = falla si existe
    index=False        # No guardes el índice de Pandas como una columna
)
print("¡Carga completada!")