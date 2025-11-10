# Ejecutar con "python -m src.scraping.scraping_tmdb"

import os
import requests
from dotenv import load_dotenv

# Cargo las variables del archivo .env
load_dotenv()

# Obtengo la clave desde el entorno
API_KEY = os.getenv("TMDB_API_KEY")

if not API_KEY:
    raise ValueError("❌ No se encontró la clave TMDB_API_KEY en el archivo .env")

# Ejemplo simple: buscar una película
def buscar_pelicula(nombre):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={nombre}&language=es-ES"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        datos = respuesta.json()
        return datos["results"][:3] 
    else:
        print("Error en la solicitud:", respuesta.status_code)
        return None

if __name__ == "__main__":
    resultados = buscar_pelicula("Alita: Battle Angel")
    print(resultados)
