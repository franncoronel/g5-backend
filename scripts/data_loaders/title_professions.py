
# Ejecutar con "python -m scripts.data_loaders.title_professions"

from src.database.entidades import motor
from src.helpers import DBLoader
from src.paths import RUTA_PRINCIPALES_2019


loader = DBLoader(motor)    # El motor de SQLAlchemy

loader.cargar_csv(
  ruta_csv=RUTA_PRINCIPALES_2019,
  tabla="profesion_titulo", # Nombre de la tabla en la BD
  renombrar={"tconst": "id_titulo","nconst": "id_persona",
             "characters": "nombre_personaje"},
  modo="append"  # 'append' = añade los datos, 'replace' = borra y crea, 'fail' = falla si existe
)