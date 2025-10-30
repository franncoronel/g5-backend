"""
* Ejecutar con: python3 -m src.database.entidades
"""
import os
import uuid
from sqlalchemy import String, create_engine
from datetime import date
from enum import Enum
from typing import List
from sqlalchemy import ForeignKey, select
from src.paths import RUTA_DB
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    Session
)


motor = create_engine(f"sqlite+pysqlite:///{RUTA_DB}", echo=True)
class Base(DeclarativeBase): # Todas las tablas definidas como clases heredan de la clase Base
    pass

class TipoTitulo(Enum):
    PELICULA = "pelicula"

class Titulo(Base):
    __tablename__ = "titulo" # Para todas las tablas se define un nombre de tabla al cual referenciamos al, por ejemplo, definir claves foráneas

    id: Mapped[str] = mapped_column(primary_key=True) # El tipo Mapped[tipo] asocia un tipo de datos de Python con su análogo en el motor de base de datos, aunque no siempre se logra hacer un mapeo directo
    tipo: Mapped[TipoTitulo]
    titulo: Mapped[str]
    duracion: Mapped[int]
    sinopsis: Mapped[str | None] = mapped_column(nullable=True, default="Sinopsis no disponible")
    poster: Mapped[str | None] = mapped_column(nullable=True, default="Imagen no disponible")
    fecha_estreno: Mapped[date]

    puntajes: Mapped[List["Puntaje"]] = relationship( # Con relationship definimos la relación entre dos tablas, como es el caso de esta relación uno a muchos
        back_populates="pelicula",
        cascade="all,delete-orphan"
        )
    profesion_titulos: Mapped[List["Profesion_Titulo"]] = relationship(back_populates="titulo")
    def __repr__(self):
        return f"Titulo(id={self.id}, tipo={self.tipo}, titulo={self.titulo!r}, duracion={self.duracion}, fecha_estreno={self.fecha_estreno})"

class Genero(Base):
    __tablename__ = "genero"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    nombre: Mapped[str]
    def __repr__(self):
        return f"Genero(id={self.id}, nombre={self.nombre!r})"

class Titulo_Genero(Base):
    __tablename__ = "titulo_genero"

    id_titulo: Mapped[str] = mapped_column(ForeignKey("titulo.id"), primary_key=True)
    id_genero: Mapped[str] = mapped_column(ForeignKey("genero.id"), primary_key=True)

    def __repr__(self):
        return f"Titulo_Genero(id_titulo={self.id_titulo}, id_genero={self.id_genero})"

class Puntaje(Base):
    __tablename__ = "puntaje"

    id: Mapped[str] = mapped_column(primary_key=True)
    id_titulo: Mapped[str] = mapped_column(ForeignKey("titulo.id")) # Al instanciar ForeignKey se pasa el nombre de la tabla, no de la clase, para relacionar las tablas.
    promedio: Mapped[float]
    cantidad_votos: Mapped[int]
    
    pelicula: Mapped["Titulo"] = relationship(back_populates="puntajes")

    def __repr__(self):
        return f"Puntaje(id={self.id}, id_titulo={self.id_titulo}, promedio={self.promedio}, cantidad_votos={self.cantidad_votos})"
class Persona(Base):
    __tablename__ = "persona"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre: Mapped[str]

    profesion_titulos: Mapped[List["Profesion_Titulo"]] = relationship(back_populates="persona")

    def __repr__(self):
        return f"Persona(id={self.id}, nombre={self.nombre!r})"

class Profesion_Titulo(Base): # También podría ser Director_Titulo, depende de las profesiones que conservemos
    __tablename__ = "profesion_titulo"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    id_titulo: Mapped[str] = mapped_column(ForeignKey("titulo.id"))
    id_persona: Mapped[str] = mapped_column(ForeignKey("persona.id"))
    id_profesion: Mapped[str] = mapped_column(ForeignKey("profesion.id"), nullable=False)
    nombre_personaje: Mapped[str | None] = mapped_column(nullable=True)

    def __repr__(self):
        return f"Profesion_Titulo(id_titulo={self.id_titulo}, id_persona={self.id_persona}, id_profesion={self.id_profesion}, nombre_personaje={self.nombre_personaje!r})"
    
class Profesion(Base):
    __tablename__ = "profesion"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    nombre: Mapped[str]
    
    def __repr__(self):
        return f"Profesion(id={self.id}, nombre={self.nombre!r})"

class Titulo_Alternativo(Base):
    __tablename__ = "titulo_alternativo"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    id_titulo: Mapped[str] = mapped_column(ForeignKey("titulo.id"))
    titulo: Mapped[str] = mapped_column(nullable=False)
    es_original: Mapped[bool] = mapped_column(nullable=False)
    region: Mapped[str | None] = mapped_column(nullable=True)
    idioma: Mapped[str | None] = mapped_column(nullable=True)

    def __repr__(self):
        return (f"Titulo_Alternativo(id_titulo={self.id_titulo}, titulo={self.titulo!r}, es_original={self.es_original}, region={self.region!r}, idioma={self.idioma!r})")

def crear_tablas() -> None:
    Base.metadata.create_all(motor) # Con esta línea podemos crear TODAS las tablas que hereden de Base

    """
        La Session establece una "conversación" con la base de datos. Dentro de una sesión podemos realizar distintas consultas y confirmarlas con session.commit().
        Es importante usar la sentencia with para que esta conexión con la base de datos se caiga al terminar de realizar operaciones
    """
    
if __name__ == "__main__":
    crear_tablas()