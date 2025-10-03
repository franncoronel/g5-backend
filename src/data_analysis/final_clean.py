"""
Correr con:
    python -m src.data_analysis.final_clean
"""
import pandas as pd
from src.helpers import DataCleaner
from src.paths import (
    RUTA_TITULO_2019,
    RUTA_ALIAS_2019,
    RUTA_CRITICAS_2019,
    RUTA_PERSONAL_2019,
    RUTA_PRINCIPALES_2019,
    RUTA_NOMBRE_2019
)

# ============================
# 🔹 1. Inicializar cleaners para cada archivo
# ============================
cleaners = {
    "Titles": DataCleaner(RUTA_TITULO_2019),
    "Akas": DataCleaner(RUTA_ALIAS_2019),
    "Ratings": DataCleaner(RUTA_CRITICAS_2019),
    "Crew": DataCleaner(RUTA_PERSONAL_2019),
    "Principals": DataCleaner(RUTA_PRINCIPALES_2019),
    "Names": DataCleaner(RUTA_NOMBRE_2019)
}

# ============================
# 🔹 2. Leer todos los DataFrames
# ============================
dfs = {name: cleaner.limpiar() for name, cleaner in cleaners.items()}

# ============================
# 🔹 3. Convertir IDs a string
# ============================
for df_name, df in dfs.items():
    for col in ["tconst", "nconst"]:
        if col in df.columns:
            df[col] = df[col].astype(str)

# ============================
# 🔹 4. Función auxiliar para mostrar cambios
# ============================
def mostrar_cambios(nombre, df_original, df_filtrado):
    total_original = len(df_original)
    total_filtrado = len(df_filtrado)
    eliminados = total_original - total_filtrado
    print(f"{nombre}: {total_original} → {total_filtrado} filas (eliminadas {eliminados})")

# ============================
# 🔹 5. Intersección de tconst
# ============================
tconst_sets = [set(dfs[name]["tconst"]) for name in ["Titles","Akas","Ratings","Crew","Principals"]]
tconst_validos = set.intersection(*tconst_sets)
print(f"Títulos comunes en todas las tablas: {len(tconst_validos):,}")

for name in ["Titles","Akas","Ratings","Crew","Principals"]:
    df_filtrado = dfs[name][dfs[name]["tconst"].isin(tconst_validos)]
    mostrar_cambios(name, dfs[name], df_filtrado)
    dfs[name] = df_filtrado

# ============================
# 🔹 6. Intersección de nconst
# ============================
nconst_sets = [set(dfs["Principals"]["nconst"]), set(dfs["Names"]["nconst"])]
nconst_validos = set.intersection(*nconst_sets)
print(f"Personas comunes en principals y names: {len(nconst_validos):,}")

for name in ["Principals","Names"]:
    df_filtrado = dfs[name][dfs[name]["nconst"].isin(nconst_validos)]
    mostrar_cambios(name, dfs[name], df_filtrado)
    dfs[name] = df_filtrado

# ============================
# 🔹 7. Sobrescribir los archivos originales usando DataCleaner
# ============================
for name, cleaner in cleaners.items():
    cleaner.guardar_csv(dfs[name], cleaner.ruta_archivo.split("/")[-1])  # sobrescribe con el mismo nombre

print("✅ Limpieza global terminada y archivos originales sobrescritos.")