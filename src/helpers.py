import pandas as pd
import os
from src.paths import DIR_DATA_PROCESADA  # carpeta de archivos procesados

'''
def leer_tsv_chunks(ruta: str):
    return pd.read_csv(ruta, sep='\t', chunksize=10000)

def guardar_csv(df, nombre_archivo,direccion_a_guardar):
    os.makedirs(direccion_a_guardar, exist_ok=True)
    df.to_csv(os.path.join(direccion_a_guardar, nombre_archivo), index=False, encoding="utf-8")
    print(f"Archivo guardado: {nombre_archivo}")
'''

class DatasetManager:
  def __init__(self,base_path=None):
    """base_path: ruta base donde se guardarán o leerán los archivos.
    Si no se especifica, se usa la raíz de los datos procesados.
    """
    self.base_path = base_path or DIR_DATA_PROCESADA     #ruta base donde se guardarán o leerán los archivos
    
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