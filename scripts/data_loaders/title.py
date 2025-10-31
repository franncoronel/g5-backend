# Ejecutar con "python -m scripts.data_loaders.title"

from src.database.entidades import motor
from src.helpers import DBLoader
from src.paths import RUTA_TITULO_2019

loader = DBLoader(motor)    # El motor de SQLAlchemy

colum_eliminar=['endYear','originalTitle']

loader.cargar_csv(
  ruta_csv=RUTA_TITULO_2019,
  tabla="titulo", # Nombre de la tabla en la BD
  renombrar={'tconst': 'id','titleType': 'tipo','primaryTitle':'titulo',
             'runtimeMinutes':'duracion','startYear':'fecha_estreno'},
  eliminar=colum_eliminar,
  modo="append"  # 'append' = añade los datos, 'replace' = borra y crea, 'fail' = falla si existe
)