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

  commandos = [ "python -m src.data_analysis.titles",
                "python -m src.data_analysis.akas",
                "python -m src.data_analysis.ratings",
                "python -m src.data_analysis.principals",
                "python -m src.data_analysis.name",
                "python -m src.data_analysis.final_clean"
              ]
  
  for cmd in commandos:
    correr_comando(cmd)
  
  print("\nTodos los scripts se ejecutaron correctamente.")

if __name__ == "__main__":
  main()
