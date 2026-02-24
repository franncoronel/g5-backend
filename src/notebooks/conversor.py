'''
Correr con:
          python -m src.notebooks.conversor
'''

import subprocess
import sys

def conversor(comandos):
  for cmd in comandos:
    print(f"\n>>> Ejecutando: {cmd}")
    result = subprocess.run(cmd, shell=True)
    
    if result.returncode != 0:
      print(f"❌ Error al ejecutar: {cmd}")
      sys.exit(result.returncode)

    print("\nEl script se ejecutó correctamente.")


def main():
  print("{:^60}".format("Conversor de formatos con jupytext"))
  print("1. Convertir .py a .ipynb")
  print("2. Convertir .ipynb a .py")
  
  opcion = int(input("Ingrese una opción: "))

  match opcion:
    case 1:
      comandos= ["jupytext --set-formats py,ipynb src/notebooks/limpieza.py",
                 "jupytext --set-formats py,ipynb src/notebooks/prueba.py",
                 "jupytext --set-formats py,ipynb src/notebooks/querys.py",
                 "jupytext --set-formats py,ipynb src/notebooks/titles.py"]
      conversor(comandos)

    case 2:
      comandos= ["jupytext --set-formats ipynb,py src/notebooks/limpieza.ipynb",
                 "jupytext --set-formats ipynb,py src/notebooks/prueba.ipynb",
                 "jupytext --set-formats ipynb,py src/notebooks/querys.ipynb",
                 "jupytext --set-formats ipynb,py src/notebooks/titles.ipynb"]
      conversor(comandos)

if __name__ == "__main__":
  main()