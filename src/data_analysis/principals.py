"""
Correr con:
    python -m src.data_analysis.principals
"""
import os
import sys
import pandas as pd


sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))

from src.paths import RUTA_PRINCIPALES
from src.paths import RUTA_TITULO_2019
from src.paths import DIR_DATA_PROCESADA
from src.helpers import DataCleaner

def main():
  # Cargo las películas 2019 procesadas
  peliculas_2019 = pd.read_csv(RUTA_TITULO_2019)
  ids_2019 = set(peliculas_2019['tconst'].astype(str))

  cleaner = DataCleaner(RUTA_PRINCIPALES, DIR_DATA_PROCESADA)
  
  columnas_a_mantener = ["tconst", "nconst", "category", "characters"]  #,"job"
  listado_trabajos=["actor", "actress", "self", "director", "writer","composer","producer"]

  df_principals = cleaner.limpiar(filtros={"tconst": list(ids_2019),
                                         "category":listado_trabajos})

  df_principals = cleaner.mantener_columnas(df_principals, columnas_a_mantener)

  # Unifico 'actor' y 'actress'
  df_principals['category'] = df_principals['category'].replace('actress', 'actor')

  # Creo Tabla de profesiones únicas
  profesiones_unicas = sorted(df_principals['category'].dropna().unique())
  df_profesiones = pd.DataFrame({"id_profesion": range(1, len(profesiones_unicas) + 1),
                                 "typeProfession": profesiones_unicas})

  # Merge para obtener id_profesion directamente
  df_rel = df_principals.merge(df_profesiones,
                               left_on="category",
                               right_on="typeProfession",
                               how="left")

  # Eliminar columnas redundantes
  df_rel = cleaner.eliminar_columnas(df_rel, ["category", "typeProfession"])

  # Guardar CSVs resultantes
  cleaner.guardar_csv(df_profesiones, "profesiones.csv")
  cleaner.guardar_csv(df_rel, "principales_profesiones_2019.csv")


if __name__ == "__main__":
  main()