# Ejecutar con "python -m src.data_loaders.title_platform"

from src.database.entidades import motor
from src.helpers import DBLoader
from src.paths import RUTA_TITULO_PLATAFORMA

loader = DBLoader(motor)    # El motor de SQLAlchemy

loader.cargar_csv(
  ruta_csv=RUTA_TITULO_PLATAFORMA,
  tabla="titulo_plataforma", # Nombre de la tabla en la BD
  renombrar={"tconst": "id_titulo"},
  modo="append"  # 'append' = añade los datos, 'replace' = borra y crea, 'fail' = falla si existe
)