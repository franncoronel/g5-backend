import pandas as pd
from ..paths import RUTA_NOMBRE
from ..helpers import leer_tsv_chunks

# Conjunto para almacenar profesiones únicas
profesiones_unicas = set()

# Leer chunk por chunk
nombres_iterable = leer_tsv_chunks(RUTA_NOMBRE)
for chunk in nombres_iterable:
    # Filtrar filas donde primaryProfession no sea nulo o '\N'
    profesiones_validas = chunk[~chunk['primaryProfession'].isna() & (chunk['primaryProfession'] != '\\N')]
    
    # Para cada fila, dividir las profesiones y añadirlas al conjunto
    for profesiones in profesiones_validas['primaryProfession']:
        profesiones_unicas.update(profesiones.split(','))

# Convertir a lista y ordenar alfabéticamente
lista_profesiones = sorted(list(profesiones_unicas))
print(f"Total de profesiones únicas encontradas: {len(lista_profesiones)}")
print("\nLista de profesiones:")
for profesion in lista_profesiones:
    print(f"- {profesion}")