
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import generos_routes, personas_routes, preferencias_routes, title_routes
from sqlalchemy.orm import Session
from src.database.entidades import Base, motor
from src.ai.embeddings import ensure_title_embeddings, get_embedder

'''
Correr con:
          python -m uvicorn src.main:app --reload
'''

app = FastAPI()

@app.on_event("startup")
def _startup():
    # Asegurar tablas
    Base.metadata.create_all(motor)
    # Warm-up del modelo para no pagar el costo en la primera request
    get_embedder()
    # Generar embeddings faltantes
    with Session(motor) as s:
        created = ensure_title_embeddings(s)
        print(f"[startup] Embeddings creados: {created}")

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
app.include_router(title_routes.router)



