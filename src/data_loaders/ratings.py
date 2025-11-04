# Ejecutar con "python -m src.data_loaders.ratings"

from src.helpers import DBLoader
from src.database.entidades import motor
from src.paths import RUTA_CRITICAS_2019

loader = DBLoader(motor)

loader.cargar_csv(
  ruta_csv=RUTA_CRITICAS_2019,
  tabla="puntaje",
  renombrar={'tconst': 'id_titulo','averageRating': 'promedio','numVotes': 'cantidad_votos'},
  modo="append",
  index=False
)