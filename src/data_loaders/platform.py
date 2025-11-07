from src.database.entidades import motor
from src.helpers import DBLoader
from src.paths import RUTA_PLATAFORMA

loader = DBLoader(motor)    # El motor de SQLAlchemy

loader.cargar_csv(
  ruta_csv=RUTA_PLATAFORMA,
  tabla="plataforma", # Nombre de la tabla en la BD
  renombrar={"id_plataforma": "id"},
  modo="append"  # 'append' = añade los datos, 'replace' = borra y crea, 'fail' = falla si existe
)