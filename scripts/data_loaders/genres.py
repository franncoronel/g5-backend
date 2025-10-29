# Ejecutar con "python -m scripts.data_loaders.genres"

from src.database.entidades import motor
from src.helpers import DBLoader
from src.paths import RUTA_GENERO_2019

# ¡IMPORTANTE!
# Asegúrate de que los nombres de las columnas en tu CSV coincidan
# EXACTAMENTE con los nombres de las columnas en tu tabla de la base de datos.
# Si no coinciden,  hay renombrarlos, arma un diccionario
#{'titulo_csv': 'nombre_columna_db'}

loader = DBLoader(motor)    # El motor de SQLAlchemy

loader.cargar_csv(
    ruta_csv=RUTA_GENERO_2019,
    tabla="genero", # Nombre de la tabla en la BD
    renombrar={"id_genre": "id", "typeGenre": "nombre"},
    modo="append"  # 'append' = añade los datos, 'replace' = borra y crea, 'fail' = falla si existe
)
