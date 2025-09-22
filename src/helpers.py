import pandas as pd
import os
from src.paths import DIR_DATA_PROCESADA  # carpeta de archivos procesados

class DatasetManager:
  def __init__(self,base_path=None):
    """base_path: ruta base donde se guardarán o leerán los archivos.
    Si no se especifica, se usa la raíz de los datos procesados.
    """
    self.base_path = base_path or DIR_DATA_PROCESADA     #ruta base donde se guardarán los archivos
    
  def leer_tsv_chunks(self, ruta_archivo):
    if not os.path.exists(ruta_archivo):
      raise FileNotFoundError(f"No se encontró el archivo: {ruta_archivo}")
    #print(f"Leyendo archivo: {ruta_archivo}")
    return pd.read_csv(ruta_archivo, sep="\t", chunksize=10000)

  def guardar_csv(self, df, nombre_archivo):
    os.makedirs(self.base_path, exist_ok=True)
    ruta = os.path.join(self.base_path, nombre_archivo)
    df.to_csv(ruta, index=False, encoding="utf-8")
    #print(f"Archivo guardado en: {ruta}")
    print(f"Archivo guardado: {nombre_archivo}")



class DataCleaner(DatasetManager):
  def __init__(self, ruta_archivo, dir_salida=None):
    super().__init__(dir_salida)
    self.ruta_archivo = ruta_archivo  # Archivo de entrada específico

  def mostrarContenidoDeUnaColumna(self, nombre_columna):  
    listado_iterable=self.leer_tsv_chunks(self.ruta_archivo)

    listado= set()

    # Leer chunk por chunk y añadir los tipos únicos al conjunto
    for chunk in listado_iterable:
      listado.update(chunk[nombre_columna].unique())
    
    # Convertir a lista y ordenar alfabéticamente
    return sorted(list(listado))
  
  def limpiar():
    pass


