
# Ejecutar con "python -m src.data_loaders.professions"

from src.database.entidades import motor
from src.helpers import DBLoader
from src.paths import RUTA_PROFESIONES


loader = DBLoader(motor)    # El motor de SQLAlchemy

loader.cargar_csv(
  ruta_csv=RUTA_PROFESIONES,
  tabla="profesion", # Nombre de la tabla en la BD
  renombrar={"id_profesion": "id","typeProfession": "nombre"},
  modo="append"  # 'append' = añade los datos, 'replace' = borra y crea, 'fail' = falla si existe
)