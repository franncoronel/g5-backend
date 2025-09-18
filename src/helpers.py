import pandas as pd

def leer_tsv_chunks(ruta: str):
    return pd.read_csv(ruta, sep='\t', chunksize=10000)