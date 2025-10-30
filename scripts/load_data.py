'''
Correr con:
          python scripts/load_data.py
'''

import subprocess
import sys

def correr_comando(comando):
  print(f"\n>>> Ejecutando: {comando}")
  result = subprocess.run(comando, shell=True)
  if result.returncode != 0:
    print(f"❌ Error al ejecutar: {comando}")
    sys.exit(result.returncode)
  
  print(f"✅ Finalizado: {comando}")

def main():

  comandos = ['python -m src.database.entidades',
               'python -m scripts.data_loaders.title',
               'python -m scripts.data_loaders.names',
               'python -m scripts.data_loaders.genres',
               'python -m scripts.data_loaders.title_genre',
               'python -m scripts.data_loaders.ratings',
               'python -m scripts.data_loaders.akas',
               'python -m scripts.data_loaders.professions',
               'python -m scripts.data_loaders.title_professions'
               ]
  
  for cmd in comandos:
    correr_comando(cmd)
  
  print("\nTodos los scripts se ejecutaron correctamente.")

if __name__ == "__main__":
  main()