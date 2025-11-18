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
from sqlalchemy.types import JSON, DateTime
from datetime import datetime
from src.paths import RUTA_DB
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    Session
)
from sqlalchemy import Enum as SqlEnum

motor = create_engine(f"sqlite+pysqlite:///{RUTA_DB}", echo=True)
class Base(DeclarativeBase): # Todas las tablas definidas como clases heredan de la clase Base
    pass

class TipoTitulo(Enum):
    PELICULA =  "movie"
    TV_MOVIE = "tvMovie"

class Titulo(Base):
    __tablename__ = "titulo" # Para todas las tablas se define un nombre de tabla al cual referenciamos al, por ejemplo, definir claves foráneas

    id: Mapped[str] = mapped_column(primary_key=True) # El tipo Mapped[tipo] asocia un tipo de datos de Python con su análogo en el motor de base de datos, aunque no siempre se logra hacer un mapeo directo
    tipo: Mapped[TipoTitulo] = mapped_column(SqlEnum(TipoTitulo), nullable=False)
    titulo: Mapped[str]
    duracion: Mapped[int]
    fecha_estreno: Mapped[date]
    idioma_original: Mapped[str | None] = mapped_column(String(10), nullable=True)
    sinopsis: Mapped[str | None] = mapped_column(nullable=True, default="Sinopsis no disponible")
    poster: Mapped[str | None] = mapped_column(String(300), nullable=True)
    backdrop: Mapped[str | None] = mapped_column(String(300), nullable=True)

    # Con relationship definimos la relación entre dos tablas, como es el caso de esta relación uno a muchos
    puntajes: Mapped[List["Puntaje"]] = relationship(back_populates="pelicula",cascade="all,delete-orphan")
    profesion_titulos: Mapped[List["Profesion_Titulo"]] = relationship(back_populates="titulo")
    generos: Mapped[List["Titulo_Genero"]] = relationship( back_populates="titulo")
    alternativos: Mapped[List["Titulo_Alternativo"]] = relationship(back_populates="titulo_rel")
    plataformas: Mapped[List["Titulo_Plataforma"]] = relationship(back_populates="titulo")

    def __repr__(self):
        return f"Titulo(id={self.id}, tipo={self.tipo}, titulo={self.titulo!r}, duracion={self.duracion}, fecha_estreno={self.fecha_estreno} , idioma_original={self.idioma_original} )"

class Genero(Base):
    __tablename__ = "genero"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    nombre: Mapped[str]

    titulos: Mapped[List["Titulo_Genero"]] = relationship(back_populates="genero")

    def __repr__(self):
        return f"Genero(id={self.id}, nombre={self.nombre!r})"

class Titulo_Genero(Base):
    __tablename__ = "titulo_genero"

    id_titulo: Mapped[str] = mapped_column(ForeignKey("titulo.id"), primary_key=True)
    id_genero: Mapped[str] = mapped_column(ForeignKey("genero.id"), primary_key=True)

    titulo: Mapped["Titulo"] = relationship(back_populates="generos")
    genero: Mapped["Genero"] = relationship(back_populates="titulos")

    def __repr__(self):
        return f"Titulo_Genero(id_titulo={self.id_titulo}, id_genero={self.id_genero})"

class Plataforma(Base):
    __tablename__ = "plataforma"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    nombre: Mapped[str]

    titulos: Mapped[List["Titulo_Plataforma"]] = relationship(back_populates="plataforma")

    def __repr__(self):
        return f"Plataforma(id={self.id}, nombre={self.nombre!r})"

class Titulo_Plataforma(Base):
    __tablename__ = "titulo_plataforma"

    id_titulo: Mapped[str] = mapped_column(ForeignKey("titulo.id"), primary_key=True)
    id_plataforma: Mapped[str] = mapped_column(ForeignKey("plataforma.id"), primary_key=True)

    titulo: Mapped["Titulo"] = relationship(back_populates="plataformas")
    plataforma: Mapped["Plataforma"] = relationship(back_populates="titulos")

    def __repr__(self):
        return f"Titulo_Plataforma(id_titulo={self.id_titulo}, id_plataforma={self.id_plataforma})"

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

    titulo: Mapped["Titulo"] = relationship(back_populates="profesion_titulos")
    persona: Mapped["Persona"] = relationship(back_populates="profesion_titulos")
    profesion: Mapped["Profesion"] = relationship(back_populates="profesion_titulos")

    def __repr__(self):
        return f"Profesion_Titulo(id_titulo={self.id_titulo}, id_persona={self.id_persona}, id_profesion={self.id_profesion}, nombre_personaje={self.nombre_personaje!r})"

class Profesion(Base):
    __tablename__ = "profesion"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    nombre: Mapped[str]

    profesion_titulos: Mapped[List["Profesion_Titulo"]] = relationship(back_populates="profesion")

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

    titulo_rel: Mapped["Titulo"] = relationship(back_populates="alternativos")

    def __repr__(self):
        return (f"Titulo_Alternativo(id_titulo={self.id_titulo}, titulo={self.titulo!r}, es_original={self.es_original}, region={self.region!r}, idioma={self.idioma!r})")

class TituloEmbedding(Base):
    __tablename__ = "titulo_embedding"

    id_titulo: Mapped[str] = mapped_column(ForeignKey("titulo.id"), primary_key=True)
    model: Mapped[str] = mapped_column(String, nullable=False)   # p.ej. "all-MiniLM-L6-v2"
    dim: Mapped[int] = mapped_column(nullable=False)             # p.ej. 384
    vector: Mapped[list[float]] = mapped_column(JSON, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    titulo: Mapped["Titulo"] = relationship()

def crear_tablas() -> None:
    Base.metadata.create_all(motor) # Con esta línea podemos crear TODAS las tablas que hereden de Base

    """
        La Session establece una "conversación" con la base de datos. Dentro de una sesión podemos realizar distintas consultas y confirmarlas con session.commit().
        Es importante usar la sentencia with para que esta conexión con la base de datos se caiga al terminar de realizar operaciones
    """

if __name__ == "__main__":
    crear_tablas()