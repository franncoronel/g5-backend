# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: .venv (3.12.3)
#     language: python
#     name: python3
# ---

# %%
import pandas as pd
import os
import sys 
import importlib

# %%
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))

# %%
import src.paths
import src.helpers
importlib.reload(src.paths)
importlib.reload(src.helpers)
from src.helpers import DataCleaner
from src.helpers import DatasetManager

# %%
from src.paths import DIR_DATA_PROCESADA
from src.paths import RUTA_TITULO_2019
from src.paths import RUTA_ALIAS_2019
from src.paths import RUTA_CRITICAS_2019
from src.paths import RUTA_PERSONAL_2019
from src.paths import RUTA_PRINCIPALES_2019
from src.paths import RUTA_NOMBRE_2019

# %%
dm = DatasetManager()
preview = dm.ver_preview(RUTA_TITULO_2019)

# %%
dm = DatasetManager()
preview = dm.ver_preview(RUTA_PRINCIPALES_2019)

# %%
dm = DatasetManager()
preview = dm.ver_preview(RUTA_NOMBRE_2019)

# %%
dm = DatasetManager()
preview = dm.ver_preview(RUTA_ALIAS_2019,n=30)

# %%
dm = DatasetManager()
preview = dm.ver_preview(RUTA_PERSONAL_2019)

# %%
dm = DatasetManager()
preview = dm.ver_preview(RUTA_CRITICAS_2019,n=30)

# %%
nombres_2019 = pd.read_csv(RUTA_NOMBRE_2019)
print(f"Nombres cargados: {len(nombres_2019):,}")

# %%
nombres_2019 = pd.read_csv(RUTA_NOMBRE_2019)
print(f"Nombres cargados: {len(nombres_2019):,}")

# %%
titulos_2019 = pd.read_csv(RUTA_TITULO_2019)
print(f"Titulos cargados: {len(titulos_2019):,}")

# %% [markdown]
# Análisis crew

# %%
crew = pd.read_csv(RUTA_PERSONAL_2019, dtype=str)
principales = pd.read_csv(RUTA_PRINCIPALES_2019, dtype=str)

# %%
coincidencias = crew.merge(
    principales,
    left_on=["tconst", "directors"],
    right_on=["tconst", "nconst"],
    how="inner")

coinciden_unicos = coincidencias[["tconst", "directors"]].drop_duplicates()

total_directores = len(crew)
total_coinciden = len(coinciden_unicos)
total_no_coinciden = total_directores - total_coinciden

porc_coinciden = (total_coinciden / total_directores) * 100 if total_directores > 0 else 0
porc_no_coinciden = (total_no_coinciden / total_directores) * 100 if total_directores > 0 else 0

print(f"Total directores en crew_2019: {total_directores:,}")
print(f"Coinciden en principals_2019:  {total_coinciden:,}  ({porc_coinciden:.2f}%)")
print(f"No coinciden:                 {total_no_coinciden:,}  ({porc_no_coinciden:.2f}%)")
