
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import anios_routes, duraciones_routes, generos_routes, personas_routes, preferencias_routes


'''
Correr con:
          python -m uvicorn src.main:app --reload
'''

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # dirección del frontend
    allow_credentials=True,
    allow_methods=["*"],  # permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # permitir todos los headers
)

app.include_router(generos_routes.router)
app.include_router(personas_routes.router)
app.include_router(preferencias_routes.router)
app.include_router(anios_routes.router)
app.include_router(duraciones_routes.router)

