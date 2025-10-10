'''
Correr con:
          python scripts/run_data_cleaning.py
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
  PYTHON = sys.executable  # usa el Python del entorno actual -> windows es python, linux es python3

  commandos = [ f"{PYTHON} -m src.data_analysis.titles",
                f"{PYTHON} -m src.data_analysis.crew",
                f"{PYTHON} -m src.data_analysis.akas",
                f"{PYTHON} -m src.data_analysis.ratings",
                f"{PYTHON} -m src.data_analysis.principals",
                f"{PYTHON} -m src.data_analysis.name",
                f"{PYTHON} -m src.data_analysis.final_clean"
              ]
  
  for cmd in commandos:
    correr_comando(cmd)
  
  print("\nTodos los scripts se ejecutaron correctamente.")

if __name__ == "__main__":
  main()
