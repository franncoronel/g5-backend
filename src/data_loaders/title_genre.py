# Ejecutar con "python -m src.data_loaders.title_genre"

from src.database.entidades import motor
from src.helpers import DBLoader
from src.paths import RUTA_TITULO_GENERO

loader = DBLoader(motor)    # El motor de SQLAlchemy

loader.cargar_csv(
  ruta_csv=RUTA_TITULO_GENERO,
  tabla="titulo_genero", # Nombre de la tabla en la BD
  renombrar={"tconst": "id_titulo","id_genre": "id_genero"},
  modo="append"  # 'append' = añade los datos, 'replace' = borra y crea, 'fail' = falla si existe
)