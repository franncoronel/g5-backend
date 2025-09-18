import os

RUTA_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Carpetas principales

DIR_DATA = os.path.join(RUTA_RAIZ, "data")

# Rutas a los archivos
RUTA_TITULO = os.path.join(DIR_DATA, "title.basics.tsv")
RUTA_NOMBRE = os.path.join(DIR_DATA, "name.basics.tsv")
RUTA_PERSONAL = os.path.join(DIR_DATA, "title.crew.tsv")
RUTA_PRINCIPALES = os.path.join(DIR_DATA, "title.principals.tsv")
RUTA_CRITICAS = os.path.join(DIR_DATA, "title.ratings.tsv")