import sqlite3
import os

# Path a la BBDD
DB_PATH = os.path.join("data", "recomendador.sqlite")

# Query para sacar idiomas que no queremos
def limpiar_idiomas():
    if not os.path.exists(DB_PATH):
        print(f"❌ Error: No encuentro la base de datos en {DB_PATH}")
        return

    print("conectando a la base de datos...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
    DELETE FROM titulo
    WHERE idioma_original IS NULL
       OR idioma_original NOT IN ('es','en','fr','it','de','ja','zh','pt','ru');
    """

    try:
        cursor.execute(query)
        filas_borradas = cursor.rowcount
        conn.commit() # ✅ Guardar cambios
        print(f"✅ ¡Listo! Se eliminaron {filas_borradas} películas que no estaban en los idiomas principales.")
    except Exception as e:
        print(f"❌ Ocurrió un error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    limpiar_idiomas()