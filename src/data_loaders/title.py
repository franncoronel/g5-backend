# Ejecutar con "python -m src.data_loaders.title"

from src.database.entidades import motor, Titulo
from src.helpers import DBLoader
from src.paths import RUTA_TITULO_2019

loader = DBLoader(motor)    # El motor de SQLAlchemy

colum_eliminar=['endYear','originalTitle','startYear']

loader.cargar_con_modelo(
  ruta_csv=RUTA_TITULO_2019,
  modelo=Titulo,  # se pasa la clase, no el nombre de tabla, así puede leer los tipos (Enum, Date, etc.).
  renombrar={'tconst': 'id',
             'titleType': 'tipo',
             'primaryTitle':'titulo',
             'runtimeMinutes':'duracion',},
  eliminar=colum_eliminar,
)