# <center>🎥 7Frames  - Recomendador de cine y series     

Backend para el proyecto final de la materia Bases de Datos de la Tecnicatura en Programación Informática de la UNSAM.  

## Integrantes  
* Francisco Coronel - PM  
* Tomas Aragusuku
* Juana Correa Luna
* Agustín Narvaez
* Joaquin Ivan Navarro
* Melody Oviedo Morales
* Carla Rocca

---  
## Tecnologías Utilizadas
* Python

---
## Estructura
`G5-BACKEND`/  
│  
├─ `data/`                         — Archivos de datos y datasets  
│     └─ `processed/`                — datos limpios/listos para análisis  
│  
├─ `src/`  
│   └─ `data_analysis`  
│  
├─ `notebooks/`                    — Jupyter Notebooks (exploración, pruebas)  
│  
├─ `README.md`  
├─ `requirements.txt`              — Dependencias de Python    
└─ `.gitignore`                    — exclusiones  

---
## Setup
### Linux/MacOS  
1. Generar un entorno virtual:  
```
python3 -m venv .venv  
```
2. Activar el entorno virtual:  
```
source .venv/bin/activate  
```
3. Una vez activado el entorno virtual, instalar las dependencias:  
```
pip install -r requirements.txt  
```  

### Windows    
1. Creo El entorno  
```  
python -m venv .venv  
```  

2. Activo el entorno  
```
.venv\Scripts\Activate  
```

3. Actualizo el pip  
```
python -m pip install --upgrade pip  
```
4. Instalo la biblioteca para comunicacion con el kernel de python

pip install jupyter ipykernel
```
5. Instalo los requerimientos  
```
pip install -r requirements.txt  
```

---