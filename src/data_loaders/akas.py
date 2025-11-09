# Ejecutar con "python -m src.data_loaders.akas"

from src.database.entidades import motor
from src.helpers import DBLoader
from src.paths import RUTA_ALIAS_2019


loader = DBLoader(motor)    # El motor de SQLAlchemy

loader.cargar_csv(
  ruta_csv=RUTA_ALIAS_2019,
  tabla="titulo_alternativo", # Nombre de la tabla en la BD
  renombrar={"tconst": "id_titulo","title": "titulo",
             "isOriginalTitle": "es_original", "language":"idioma"},
  modo="append",  # 'append' = añade los datos, 'replace' = borra y crea, 'fail' = falla si existe
  auto_id=True
)