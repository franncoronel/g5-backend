'''
TODO:PARA CORRER EL CÓDIGO CON EL SIG. COMANDO EN TERMINAL -> 
      python -m src.data_analysis.platform
'''
import os
import sys
import pandas as pd

# Ajustar path para poder importar módulos del proyecto
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))

from src.helpers import DataCleaner
from src.paths import DIR_DATA_PROCESADA
from src.paths import RUTA_TITULO_2019 as RUTA_TITULOS
from src.paths import RUTA_PLATFORM as RUTA_PLATAFORMAS


def main():
    cleaner = DataCleaner(RUTA_TITULOS, DIR_DATA_PROCESADA)

    # ------------------------------------------------------------------
    # 1️⃣ Leemos ambos CSVs
    # ------------------------------------------------------------------
    df_titulos = pd.read_csv(RUTA_TITULOS)
    df_plataformas = pd.read_csv(RUTA_PLATAFORMAS)

    print(f"📁 Titulos: {len(df_titulos):,}")
    print(f"📁 Plataformas: {len(df_plataformas):,}")

    # ------------------------------------------------------------------
    # 2️⃣ Validar coincidencias entre ambos archivos
    # ------------------------------------------------------------------
    df_merge = pd.merge(
        df_plataformas,
        df_titulos[["tconst", "primaryTitle"]],
        on=["tconst", "primaryTitle"],
        how="inner"
    )

    print(f"✅ Coincidencias encontradas: {len(df_merge):,}")

    # Mostrar los que no coincidieron
    df_no_coinciden = df_plataformas.merge(
        df_titulos[["tconst", "primaryTitle"]],
        on=["tconst", "primaryTitle"],
        how="left",
        indicator=True
    ).query("_merge == 'left_only'")[["tconst", "primaryTitle"]]

    if not df_no_coinciden.empty:
        print("\n⚠️ Registros del CSV de plataformas sin coincidencia en títulos:")
        for _, fila in df_no_coinciden.iterrows():
            print(f"  - {fila['tconst']} | {fila['primaryTitle']}")

    # ------------------------------------------------------------------
    # 3️⃣ Limpiar y preparar datos válidos
    # ------------------------------------------------------------------
    df_merge = cleaner.columna_como_lista(df_merge, "plataformas")

    # Extraer plataformas únicas
    plataformas_unicas = sorted({
        p.strip()
        for lista in df_merge["plataformas"]
        if isinstance(lista, list)
        for p in lista
        if p.strip().lower() != "no disponible" and p.strip() != ""
    })

    df_plataformas_unicas = pd.DataFrame({
        "id_plataforma": range(1, len(plataformas_unicas) + 1),
        "nombre": plataformas_unicas
    })

    # ------------------------------------------------------------------
    # 4️⃣ Crear tabla intermedia (solo coincidencias válidas)
    # ------------------------------------------------------------------
    df_relacional = df_merge[["tconst", "plataformas"]].explode("plataformas")
    df_relacional["plataformas"] = df_relacional["plataformas"].str.strip()

    # Unir con IDs de plataforma
    df_relacional = df_relacional.merge(
        df_plataformas_unicas,
        left_on="plataformas",
        right_on="nombre",
        how="inner"
    )[["tconst", "id_plataforma"]].drop_duplicates()

    # ------------------------------------------------------------------
    # 5️⃣ Guardar resultados
    # ------------------------------------------------------------------
    cleaner.guardar_csv(df_plataformas_unicas, "plataforma.csv")
    cleaner.guardar_csv(df_relacional, "titulo_plataforma.csv")

    print("\n✅ Archivos generados correctamente:")
    print("   - plataforma.csv")
    print("   - titulo_plataforma.csv")

if __name__ == "__main__":
    main()
