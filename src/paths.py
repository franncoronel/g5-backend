import os

RUTA_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Carpetas principales
DIR_DATA = os.path.join(RUTA_RAIZ, "data")

# Carpeta donde se guardarán los archivos procesados
DIR_DATA_PROCESADA = os.path.join(DIR_DATA, "processed")

# Carpeta de caché
DIR_CACHE = os.path.join(DIR_DATA, "cache_file")

# Rutas a los archivos
RUTA_TITULO = os.path.join(DIR_DATA, "title.basics.tsv")
RUTA_NOMBRE = os.path.join(DIR_DATA, "name.basics.tsv")
RUTA_PRINCIPALES = os.path.join(DIR_DATA, "title.principals.tsv")
RUTA_CRITICAS = os.path.join(DIR_DATA, "title.ratings.tsv")
RUTA_ALIAS= os.path.join(DIR_DATA,"title.akas.tsv")
#RUTA_PERSONAL = os.path.join(DIR_DATA, "title.crew.tsv")
RUTA_PLATFORM=os.path.join(DIR_DATA,"peliculas_cargadas.csv")

# Ruta de archivos filtrados
RUTA_ALIAS_2019 = os.path.join(DIR_DATA_PROCESADA,"alias_2019.csv")
RUTA_CRITICAS_2019 = os.path.join(DIR_DATA_PROCESADA,"criticas_2019.csv")
RUTA_GENERO_2019 = os.path.join(DIR_DATA_PROCESADA, "generos_2019.csv")
RUTA_NOMBRE_2019 = os.path.join(DIR_DATA_PROCESADA, "nombres_2019.csv")
RUTA_TITULO_2019 = os.path.join(DIR_DATA_PROCESADA,"peliculas_2019.csv")
RUTA_PRINCIPALES_2019 = os.path.join(DIR_DATA_PROCESADA,"principales_profesiones_2019.csv")
RUTA_TITULO_GENERO = os.path.join(DIR_DATA_PROCESADA, "rel_titulos_generos.csv")
RUTA_PROFESIONES= os.path.join(DIR_DATA_PROCESADA,"profesiones.csv")
RUTA_TITULO_PLATAFORMA=os.path.join(DIR_DATA_PROCESADA,"titulo_plataforma.csv")
RUTA_PLATAFORMA=os.path.join(DIR_DATA_PROCESADA,"plataforma.csv")

# Base de datos
RUTA_DB = os.path.join(DIR_DATA, "recomendador.sqlite")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
DB_PATH = os.path.join(BASE_DIR, "data", "recomendador.sqlite")