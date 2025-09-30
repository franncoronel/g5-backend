import os

RUTA_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Carpetas principales
DIR_DATA = os.path.join(RUTA_RAIZ, "data")

# Carpeta donde se guardarán los archivos procesados
DIR_DATA_PROCESADA = os.path.join(DIR_DATA, "processed")

# Rutas a los archivos
RUTA_TITULO = os.path.join(DIR_DATA, "title.basics.tsv")
RUTA_NOMBRE = os.path.join(DIR_DATA, "name.basics.tsv")
RUTA_PERSONAL = os.path.join(DIR_DATA, "title.crew.tsv")
RUTA_PRINCIPALES = os.path.join(DIR_DATA, "title.principals.tsv")
RUTA_CRITICAS = os.path.join(DIR_DATA, "title.ratings.tsv")
RUTA_ALIAS= os.path.join(DIR_DATA,"title.akas.tsv")

# Ruta de archivos filtrados
RUTA_TITULO_2019 = os.path.join(DIR_DATA_PROCESADA,"peliculas_2019.csv")
RUTA_ALIAS_2019 = os.path.join(DIR_DATA_PROCESADA,"alias_2019.csv")
RUTA_CRITICAS_2019 = os.path.join(DIR_DATA_PROCESADA,"criticas_2019.csv")
RUTA_PERSONAL_2019 = os.path.join(DIR_DATA_PROCESADA,"crew_2019.csv")
RUTA_PRINCIPALES_2019 =os.path.join(DIR_DATA_PROCESADA,"principales_2019.csv")
RUTA_NOMBRE_2019 = os.path.join(DIR_DATA_PROCESADA, "nombres_2019.csv")