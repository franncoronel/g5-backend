"""
Correr con:
    python -m src.data_analysis.name
"""
import os
import sys
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))

from src.paths import RUTA_NOMBRE
from src.paths import RUTA_PRINCIPALES_2019
from src.paths import DIR_DATA_PROCESADA

from src.helpers import DataCleaner

def main():
  df_principals = pd.read_csv(RUTA_PRINCIPALES_2019)  #de aca saco los "nconst"

  cleaner = DataCleaner(RUTA_NOMBRE , DIR_DATA_PROCESADA)

  columnas_a_mantener = ['nconst', 'primaryName', 'birthYear','primaryProfession']

  nconsts_relevantes = set(df_principals["nconst"].astype(str))


  df_names = cleaner.limpiar(filtros={'nconst': list(nconsts_relevantes)})
  df_names = cleaner.mantener_columnas(df_names,columnas_a_mantener)


  cleaner.guardar_csv(df_names, "nombres_2019.csv")
if __name__ == "__main__":
  main()