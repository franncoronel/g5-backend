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

  def ver_preview(self, ruta_archivo, n=4, sep="\t", **kwargs):
    """Muestra las columnas y las primeras `n` filas de un archivo TSV/CSV."""
    if not os.path.exists(ruta_archivo):
      raise FileNotFoundError(f"No se encontró el archivo: {ruta_archivo}")
      
    df = pd.read_csv(ruta_archivo, sep=sep, nrows=n, **kwargs)
    print("Columnas:", list(df.columns))
    print("\nPrimeras filas:")
    print(df.head(n))
    return df


class DataCleaner(DatasetManager):
  def __init__(self, ruta_archivo, dir_salida=None):
    super().__init__(dir_salida)
    self.ruta_archivo = ruta_archivo  # Archivo de entrada específico

  def valores_unicos_columna(self, nombre_columna):
    """Devuelve los valores únicos de una columna en el archivo cargado."""
    listado_iterable=self.leer_tsv_chunks(self.ruta_archivo)

    listado= set()

    # Leer chunk por chunk y añadir los tipos únicos al conjunto
    for chunk in listado_iterable:
      listado.update(chunk[nombre_columna].dropna().unique())   # ignora NaN
    
    # Convertir a lista y ordenar alfabéticamente
    return sorted(list(listado))
  
  def limpiar(self, filtros=None): 
    """Filtra el DataFrame del archivo cargado según los valores que queremos mantener
    filtros (dict): condiciones de filtrado {columna: valor} o {columna: [valores]}
    ej:{"titleType": ["movie", "tvMovie"], "isAdult": 0}"""
    listado_iterable=self.leer_tsv_chunks(self.ruta_archivo)
    
    df_limpio = []

    for chunk in listado_iterable:
      if filtros:
        for col, val in filtros.items():
          if isinstance(val, list):               # evalua si es una lista
            chunk = chunk[chunk[col].isin(val)]
          else:                                   #sino, filtra por igualdad
            chunk = chunk[chunk[col] == val]
      if not chunk.empty:
        df_limpio.append(chunk)
    
    df_final = pd.concat(df_limpio, ignore_index=True)

    return df_final

  def contar_nulos(self, df, columna):
    nulos_N = df[df[columna] == '\\N'].shape[0]  # Contar '\N'
    nulos_nan = df[columna].isna().sum()         # Contar NaN
    total = nulos_N + nulos_nan
    porcentaje = (total / len(df)) * 100
    return {
        'Valores \\N': nulos_N,
        'Valores NaN': nulos_nan,
        'Total Nulos': total,
        'Porcentaje': f"{porcentaje:.2f}%"
    }
  
  def mostrar_nulos(self, df):
    print("Análisis de valores nulos por columna:")
    print("-" * 50)

    for columna in df.columns:
      resultados = self.contar_nulos(df, columna)
      print(f"\nColumna: {columna}")
      print(f"- Valores '\\N': {resultados['Valores \\N']:,}")
      print(f"- Valores NaN: {resultados['Valores NaN']:,}")
      print(f"- Total nulos: {resultados['Total Nulos']:,}")
      print(f"- Porcentaje: {resultados['Porcentaje']}")

    # Mostrar también cuántos registros tienen al menos un valor nulo
    registros_con_nulos = df[df.apply(lambda x: (x == '\\N').any() or x.isna().any(), axis=1)]
    print(f"\nRegistros con al menos un valor nulo: {len(registros_con_nulos):,} ({(len(registros_con_nulos)/len(df)*100):.2f}% del total)")


  def limpiar_nulos(self, df, columnas, nulo_especial='\\N'):
    """Elimina registros que tengan valores nulos en las columnas especificadas"""
    if df.empty:
      return df

    mascara = True # Comenzamos con todos los registros
    for col in columnas:
      # Filtrar tanto '\N' como NaN
      mascara = mascara & (df[col] != nulo_especial) & (~df[col].isna())

    df_limpio = df[mascara].copy()
    
    return df_limpio
  
  def mostrar_registros_filtrados(self,df_sin_filtrar,df_filtrado):
    registros_eliminados = len(df_sin_filtrar) - len(df_filtrado)
    print(f"Registros originales: {len(df_sin_filtrar):,}")
    print(f"Registros después de eliminar nulos: {len(df_filtrado):,}")
    print(f"Registros eliminados: {registros_eliminados:,} ({(registros_eliminados/len(df_sin_filtrar)*100):.2f}%)")

  def filtrar_dataframe(self, df, filtros):
    """Filtra un DataFrame según un diccionario de condiciones.
    df: DataFrame a filtrar
    filtros (dict): {columna: valor} o {columna: [valores]}.
    """

    df_filtrado = df.copy()

    for col, val in filtros.items():
        if isinstance(val, list):
            df_filtrado = df_filtrado[df_filtrado[col].isin(val)]
        else:
            df_filtrado = df_filtrado[df_filtrado[col] == val]

    return df_filtrado
  
  def eliminar_columnas(self,df,columnas):
    """Elimina columnas de un DataFrame."""

    return df.drop(columns=columnas, errors='ignore') # errors='ignore' evita errores si alguna columna no existe
  
  def mantener_columnas(self, df, columnas):
    """Mantiene solo las columnas especificadas en el DataFrame."""
    return df[columnas]
  