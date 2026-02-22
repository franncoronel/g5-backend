# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: .venv (3.12.3)
#     language: python
#     name: python3
# ---

# %%
import pandas as pd
from sqlalchemy import create_engine, select, func,text
from sqlalchemy.orm import Session
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))

# %%
from src.database.entidades import (motor,Titulo,Genero,Titulo_Genero,Puntaje,Persona,
                                    Profesion,Profesion_Titulo,Titulo_Alternativo)

session = Session(motor)

# %% [markdown]
# Todos los títulos

# %%
titulos = session.execute(select(Titulo)).scalars().all()
df_titulos = pd.DataFrame([{
    "id": t.id,
    "tipo": t.tipo.value,
    "titulo": t.titulo,
    "fecha_estreno": t.fecha_estreno,
    "duracion": t.duracion
} for t in titulos])
display(df_titulos.head())

# %% [markdown]
# Filtrar películas por tipo

# %%
peliculas = session.execute(
    select(Titulo).where(Titulo.tipo == 'PELICULA')
).scalars().all()

print(f"🎞️ Total películas: {len(peliculas)}")
[p.titulo for p in peliculas[:10]]

# %%
peliculas = session.execute(
    select(Titulo).where(Titulo.tipo == 'TV_MOVIE')
).scalars().all()

print(f"🎞️ Total películas: {len(peliculas)}")
[p.titulo for p in peliculas[:10]]

# %% [markdown]
# Mostrar géneros de un título

# %%
titulo_id = 'tt10004372'
generos = session.execute(
    select(Genero.nombre)
    .join(Titulo_Genero)
    .where(Titulo_Genero.id_titulo == titulo_id)
).scalars().all()

print(f"Géneros asociados a {titulo_id}: {generos}")

# %%
titulo_id = 'tt0385887'
generos = session.execute(
    select(Genero.nombre)
    .join(Titulo_Genero)
    .where(Titulo_Genero.id_titulo == titulo_id)
).scalars().all()

print(f"Géneros asociados a {titulo_id}: {generos}")

# %% [markdown]
# Puntaje de un título

# %%
puntaje = session.execute(
    select(Puntaje.promedio, Puntaje.cantidad_votos)
    .where(Puntaje.id_titulo == titulo_id)
).first()

puntaje if puntaje else "Sin puntaje"

# %% [markdown]
# Personas que participaron en un título

# %%
personas = session.execute(
    select(Persona.nombre, Profesion.nombre, Profesion_Titulo.nombre_personaje)
    .join(Profesion_Titulo, Persona.id == Profesion_Titulo.id_persona)
    .join(Profesion, Profesion.id == Profesion_Titulo.id_profesion)
    .where(Profesion_Titulo.id_titulo == titulo_id)
).all()

pd.DataFrame(personas, columns=["Persona", "Profesión", "Personaje"])

# %% [markdown]
# Cantidad de títulos por tipo

# %%
session.execute(select(Titulo.tipo, func.count()).group_by(Titulo.tipo)).all()

# %% [markdown]
# Cantidad de títulos por género

# %%
session.execute(
    select(Genero.nombre, func.count(Titulo_Genero.id_titulo))
    .join(Titulo_Genero)
    .group_by(Genero.nombre)
).all()

# %% [markdown]
# búsqueda por nombre alternativo parcial

# %%
busqueda = "Retrato de una mujer en llamas"

resultados = session.execute(
    select(Titulo.id, Titulo.titulo, Titulo_Alternativo.titulo, Titulo_Alternativo.region, Titulo_Alternativo.idioma)
    .join(Titulo_Alternativo, Titulo.id == Titulo_Alternativo.id_titulo)
    .where(Titulo_Alternativo.titulo.ilike(f"%{busqueda}%"))
).all()

df_akas = pd.DataFrame(resultados, columns=["ID", "Título Original", "AKA", "Región", "Idioma"])
display(df_akas if not df_akas.empty else "❌ No se encontraron coincidencias.")

# %%
resultados = session.execute(
  select(Persona.nombre, Profesion.nombre, Titulo.titulo)
  .join(Profesion_Titulo, Persona.id == Profesion_Titulo.id_persona)
  .join(Profesion, Profesion.id == Profesion_Titulo.id_profesion)
  .join(Titulo, Titulo.id == Profesion_Titulo.id_titulo)
  .limit(10)
).all()

df_profesiones = pd.DataFrame(resultados, columns=["Persona", "Profesión", "Título"])
display(df_profesiones)

# %%
resultados = session.execute(
  select(Titulo.titulo, Puntaje.promedio, Puntaje.cantidad_votos)
  .join(Puntaje, Titulo.id == Puntaje.id_titulo)
  .order_by(Puntaje.cantidad_votos.desc())
  .limit(10)
).all()

df_puntajes = pd.DataFrame(resultados, columns=["Título", "Rating", "Votos"])
display(df_puntajes)

# %%
resultados = session.execute(
  select(
    Titulo.titulo,
    Genero.nombre,
    Persona.nombre,
    Profesion.nombre,
    Puntaje.promedio
  )
  .join(Titulo_Genero, Titulo.id == Titulo_Genero.id_titulo, isouter=True)
  .join(Genero, Genero.id == Titulo_Genero.id_genero, isouter=True)
  .join(Profesion_Titulo, Titulo.id == Profesion_Titulo.id_titulo, isouter=True)
  .join(Persona, Persona.id == Profesion_Titulo.id_persona, isouter=True)
  .join(Profesion, Profesion.id == Profesion_Titulo.id_profesion, isouter=True)
  .join(Puntaje, Titulo.id == Puntaje.id_titulo, isouter=True)
  .limit(20)
).all()

df_integridad = pd.DataFrame(resultados, columns=["Título", "Género", "Persona", "Profesión", "Rating"])
display(df_integridad)

# %%
tablas = ["titulo", "genero", "titulo_genero", "persona", "profesion", 
          "profesion_titulo", "puntaje", "titulo_alternativo"]

for tabla in tablas:
  total = session.execute(text(f"SELECT COUNT(*) FROM {tabla}")).scalar()
  print(f"{tabla:<20} → {total:,} registros")

# %%
session.close()
print("Sesión cerrada correctamente.")
