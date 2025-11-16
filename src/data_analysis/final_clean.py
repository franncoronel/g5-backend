"""
Correr con:
    python -m src.data_analysis.final_clean
"""
import os
import pandas as pd
from src.paths import (
    DIR_DATA_PROCESADA, RUTA_PELICULAS_TMDB, RUTA_TITULO_2019, RUTA_ALIAS_2019, RUTA_CRITICAS_2019,
    RUTA_PRINCIPALES_2019, RUTA_NOMBRE_2019
)

def main():
    # ========== 1. Cargar todos los CSV ==========
    print("🔹 Cargando archivos procesados...")
    peliculas = pd.read_csv(RUTA_TITULO_2019, dtype=str)
    alias = pd.read_csv(RUTA_ALIAS_2019, dtype=str)
    criticas = pd.read_csv(RUTA_CRITICAS_2019, dtype=str)
    principals = pd.read_csv(RUTA_PRINCIPALES_2019, dtype=str)
    nombres = pd.read_csv(RUTA_NOMBRE_2019, dtype=str)

    # ========== 2. Intersección de tconst ==========
    print("🔹 Calculando intersección de tconst...")
    inter_tconst = set(peliculas["tconst"]) \
        & set(alias["tconst"]) \
        & set(criticas["tconst"]) \
        & set(principals["tconst"])

    print(f"✅ Total tconst comunes: {len(inter_tconst):,}")

    # ========== 3. Intersección de nconst ==========
    print("🔹 Calculando intersección de nconst...")
    inter_nconst = set(principals["nconst"]) & set(nombres["nconst"])
    print(f"✅ Total nconst comunes: {len(inter_nconst):,}")

    # ========== 4. Filtrar los DataFrames ==========
    print("🔹 Filtrando registros...")

    peliculas = peliculas[peliculas["tconst"].isin(inter_tconst)]
    alias = alias[alias["tconst"].isin(inter_tconst)]
    criticas = criticas[criticas["tconst"].isin(inter_tconst)]
    principals = principals[principals["tconst"].isin(inter_tconst) & principals["nconst"].isin(inter_nconst)]
    nombres = nombres[nombres["nconst"].isin(inter_nconst)]

    # ========== 5. Agregar columnas desde RUTA_PELICULAS_TMDB ==========
    print("\n🔹 Cargando datos faltantes en películas (poster, sinopsis, idioma, backdrop)...")

    try:
        df_tmdb = pd.read_csv(RUTA_PELICULAS_TMDB, sep=",", low_memory=False)

        columnas_necesarias = ['tconst', 'primaryTitle', 'fecha_estreno', 'sinopsis', 'poster', 'idioma_original', 'backdrop']
        df_tmdb =df_tmdb[columnas_necesarias]

        # Merge para agregar columnas
        peliculas_merged = pd.merge(
            peliculas,
            df_tmdb,
            on=['tconst', 'primaryTitle'],
            how='left',
            indicator=True
        )

        # detectar registros faltantes
        faltantes = peliculas_merged[peliculas_merged['_merge'] != 'both']
        if not faltantes.empty:
            total = len(peliculas_merged)
            faltantes_count = len(faltantes)
            porcentaje = (faltantes_count / total) * 100

            print(f"Registros sin coincidencia con RUTA_PELICULAS_TMDB:")
            print(f"→ Total registros: {total}")
            print(f"→ Faltantes: {faltantes_count} ({porcentaje:.2f}%)")

        # Eliminar columna auxiliar del merge
        peliculas_merged.drop(columns=['_merge'], inplace=True)

        # Si la fecha de estreno está vacía, cargar con 2019
        if 'fecha_estreno' in peliculas_merged.columns:
            peliculas_merged['fecha_estreno'] = peliculas_merged['fecha_estreno'].fillna('2019')

        peliculas = peliculas_merged

    except Exception as e:
        print(f"❌ Error al combinar con TMDB actualizado: {e}")
        
    # ========== 6. Sobrescribir los archivos ==========
    print("💾 Sobrescribiendo archivos...")

    peliculas.to_csv(RUTA_TITULO_2019, index=False, encoding="utf-8")
    alias.to_csv(RUTA_ALIAS_2019, index=False, encoding="utf-8")
    criticas.to_csv(RUTA_CRITICAS_2019, index=False, encoding="utf-8")
    principals.to_csv(RUTA_PRINCIPALES_2019, index=False, encoding="utf-8")
    nombres.to_csv(RUTA_NOMBRE_2019, index=False, encoding="utf-8")

    # ========== 6. Resumen ==========
    print("\n✅ Limpieza cruzada completada.")
    print(f"Películas finales: {len(peliculas):,}")
    print(f"Alias finales: {len(alias):,}")
    print(f"Críticas finales: {len(criticas):,}")
    print(f"Principales finales: {len(principals):,}")
    print(f"Nombres finales: {len(nombres):,}")

if __name__ == "__main__":
    main()